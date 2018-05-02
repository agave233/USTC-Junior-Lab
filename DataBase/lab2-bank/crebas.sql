/*==============================================================*/
/* DBMS name:      ORACLE Version 11g                           */
/* Created on:     2018/5/2 20:37:23                            */
/*==============================================================*/


alter table "account"
   drop constraint FK_ACCOUNT_ACCOUNT_I_STAFF;

alter table "borrow"
   drop constraint FK_BORROW_BORROW_LOAN;

alter table "borrow"
   drop constraint FK_BORROW_BORROW2_CLIENT;

alter table "check_account"
   drop constraint FK_CHECK_AC_ACCOUNT_T_ACCOUNT;

alter table "client"
   drop constraint FK_CLIENT_RELATION2_LINKMAN;

alter table "department"
   drop constraint FK_DEPARTME_DEPT_SET_SUBBRANC;

alter table "linkman"
   drop constraint FK_LINKMAN_RELATION_CLIENT;

alter table "loan"
   drop constraint FK_LOAN_RELATIONS_STAFF;

alter table "loan"
   drop constraint FK_LOAN_PROVIDE_SUBBRANC;

alter table "loan_pay"
   drop constraint FK_LOAN_PAY_LOAN_PAY_LOAN;

alter table "manager"
   drop constraint FK_MANAGER_BELONG_STAFF;

alter table "open_account"
   drop constraint FK_OPEN_ACC_OPEN_ACCO_ACCOUNT;

alter table "open_account"
   drop constraint FK_OPEN_ACC_OPEN_ACCO_CLIENT;

alter table "saving_account"
   drop constraint FK_SAVING_A_ACCOUNT_T_ACCOUNT;

alter table "staff"
   drop constraint FK_STAFF_HAVE_DEPARTME;

alter table "staff"
   drop constraint FK_STAFF_MANAGER_MANAGER;

drop index "account_in_charge_FK";

drop table "account" cascade constraints;

drop index "borrow2_FK";

drop index "borrow_FK";

drop table "borrow" cascade constraints;

drop table "check_account" cascade constraints;

drop index "relation2_FK";

drop table "client" cascade constraints;

drop index "dept_set_FK";

drop table "department" cascade constraints;

drop table "linkman" cascade constraints;

drop index "Relationship_8_FK";

drop index "provide_FK";

drop table "loan" cascade constraints;

drop table "loan_pay" cascade constraints;

drop table "manager" cascade constraints;

drop index "open_account2_FK";

drop index "open_account_FK";

drop table "open_account" cascade constraints;

drop table "saving_account" cascade constraints;

drop index "manager_FK";

drop index "have_FK";

drop table "staff" cascade constraints;

drop table "subbranch" cascade constraints;

/*==============================================================*/
/* Table: "account"                                             */
/*==============================================================*/
create table "account" 
(
   "account_id"         VARCHAR2(20)         not null,
   "staff_id"           VARCHAR2(20),
   "account_money"      NUMBER(8,2)          not null,
   "account_date"       DATE                 not null,
   "account_recent_date" DATE,
   constraint PK_ACCOUNT primary key ("account_id")
);

/*==============================================================*/
/* Index: "account_in_charge_FK"                                */
/*==============================================================*/
create index "account_in_charge_FK" on "account" (
   "staff_id" ASC
);

/*==============================================================*/
/* Table: "borrow"                                              */
/*==============================================================*/
create table "borrow" 
(
   "loan_id"            VARCHAR2(20)         not null,
   "client-_id"         VARCHAR2(20)         not null,
   constraint PK_BORROW primary key ("loan_id", "client-_id")
);

/*==============================================================*/
/* Index: "borrow_FK"                                           */
/*==============================================================*/
create index "borrow_FK" on "borrow" (
   "loan_id" ASC
);

/*==============================================================*/
/* Index: "borrow2_FK"                                          */
/*==============================================================*/
create index "borrow2_FK" on "borrow" (
   "client-_id" ASC
);

/*==============================================================*/
/* Table: "check_account"                                       */
/*==============================================================*/
create table "check_account" 
(
   "account_id"         VARCHAR2(20)         not null,
   "staff_id"           VARCHAR2(20),
   "account_money"      NUMBER(8,2)          not null,
   "account_date"       DATE                 not null,
   "account_recent_date" DATE,
   "check_account_overdraft" NUMBER(8,2)          not null,
   "check_account_branch" VARCHAR2(40)         not null,
   "check_account_clientID" VARCHAR2(20)         not null,
   constraint PK_CHECK_ACCOUNT primary key ("account_id"),
   constraint AK_IDENTIFIER_1_CHECK_AC unique ("check_account_branch", "check_account_clientID")
);

/*==============================================================*/
/* Table: "client"                                              */
/*==============================================================*/
create table "client" 
(
   "client-_id"         VARCHAR2(20)         not null,
   "lin_client-_id"     VARCHAR2(20),
   "client_name"        VARCHAR2(20)         not null,
   "client_tel"         VARCHAR2(20)         not null,
   "client_addr"        VARCHAR2(40)         not null,
   constraint PK_CLIENT primary key ("client-_id")
);

/*==============================================================*/
/* Index: "relation2_FK"                                        */
/*==============================================================*/
create index "relation2_FK" on "client" (
   "lin_client-_id" ASC
);

/*==============================================================*/
/* Table: "department"                                          */
/*==============================================================*/
create table "department" 
(
   "dept_id"            VARCHAR2(10)         not null,
   "branch_name"        VARCHAR2(40),
   "dept_name"          VARCHAR2(20)         not null,
   "dept_type"          VARCHAR2(10)         not null,
   "dept_manager_id"    VARCHAR2(20)         not null,
   constraint PK_DEPARTMENT primary key ("dept_id")
);

/*==============================================================*/
/* Index: "dept_set_FK"                                         */
/*==============================================================*/
create index "dept_set_FK" on "department" (
   "branch_name" ASC
);

/*==============================================================*/
/* Table: "linkman"                                             */
/*==============================================================*/
create table "linkman" 
(
   "client-_id"         VARCHAR2(20)         not null,
   "linkman_name"       VARCHAR2(20)         not null,
   "linkman_phone"      VARCHAR2(20)         not null,
   "linkman_email"      VARCHAR2(20),
   "linkman_relation"   VARCHAR2(10)         not null,
   constraint PK_LINKMAN primary key ("client-_id")
);

/*==============================================================*/
/* Table: "loan"                                                */
/*==============================================================*/
create table "loan" 
(
   "loan_id"            VARCHAR2(20)         not null,
   "branch_name"        VARCHAR2(40),
   "staff_id"           VARCHAR2(20),
   "load_money"         NUMBER(8,2)          not null,
   constraint PK_LOAN primary key ("loan_id")
);

/*==============================================================*/
/* Index: "provide_FK"                                          */
/*==============================================================*/
create index "provide_FK" on "loan" (
   "branch_name" ASC
);

/*==============================================================*/
/* Index: "Relationship_8_FK"                                   */
/*==============================================================*/
create index "Relationship_8_FK" on "loan" (
   "staff_id" ASC
);

/*==============================================================*/
/* Table: "loan_pay"                                            */
/*==============================================================*/
create table "loan_pay" 
(
   "loan_id"            VARCHAR2(20)         not null,
   "loan_pay_money"     NUMBER(8,2)          not null,
   "load_pay_date"      DATE                 not null,
   constraint PK_LOAN_PAY primary key ("loan_id")
);

/*==============================================================*/
/* Table: "manager"                                             */
/*==============================================================*/
create table "manager" 
(
   "staff_id"           VARCHAR2(20)         not null,
   "dept_id"            VARCHAR2(10),
   "staff_name"         VARCHAR2(20)         not null,
   "staff_addr"         VARCHAR2(40)         not null,
   "staff_tel"          VARCHAR2(20)         not null,
   "staff_workday"      DATE                 not null,
   constraint PK_MANAGER primary key ("staff_id")
);

/*==============================================================*/
/* Table: "open_account"                                        */
/*==============================================================*/
create table "open_account" 
(
   "account_id"         VARCHAR2(20)         not null,
   "client-_id"         VARCHAR2(20)         not null,
   constraint PK_OPEN_ACCOUNT primary key ("account_id", "client-_id")
);

/*==============================================================*/
/* Index: "open_account_FK"                                     */
/*==============================================================*/
create index "open_account_FK" on "open_account" (
   "account_id" ASC
);

/*==============================================================*/
/* Index: "open_account2_FK"                                    */
/*==============================================================*/
create index "open_account2_FK" on "open_account" (
   "client-_id" ASC
);

/*==============================================================*/
/* Table: "saving_account"                                      */
/*==============================================================*/
create table "saving_account" 
(
   "account_id"         VARCHAR2(20)         not null,
   "staff_id"           VARCHAR2(20),
   "account_money"      NUMBER(8,2)          not null,
   "account_date"       DATE                 not null,
   "account_recent_date" DATE,
   "saving_accounlit_rate" FLOAT                not null,
   "saving_account_curr_type" VARCHAR2(10)         not null,
   "saving_account_branch" VARCHAR2(40)         not null,
   "saving_account_clientID" VARCHAR2(20)         not null,
   constraint PK_SAVING_ACCOUNT primary key ("account_id"),
   constraint AK_IDENTIFIER_1_SAVING_A unique ("saving_account_branch", "saving_account_clientID")
);

/*==============================================================*/
/* Table: "staff"                                               */
/*==============================================================*/
create table "staff" 
(
   "staff_id"           VARCHAR2(20)         not null,
   "dept_id"            VARCHAR2(10),
   "man_staff_id"       VARCHAR2(20),
   "staff_name"         VARCHAR2(20)         not null,
   "staff_addr"         VARCHAR2(40)         not null,
   "staff_tel"          VARCHAR2(20)         not null,
   "staff_workday"      DATE                 not null,
   constraint PK_STAFF primary key ("staff_id")
);

/*==============================================================*/
/* Index: "have_FK"                                             */
/*==============================================================*/
create index "have_FK" on "staff" (
   "dept_id" ASC
);

/*==============================================================*/
/* Index: "manager_FK"                                          */
/*==============================================================*/
create index "manager_FK" on "staff" (
   "man_staff_id" ASC
);

/*==============================================================*/
/* Table: "subbranch"                                           */
/*==============================================================*/
create table "subbranch" 
(
   "branch_name"        VARCHAR2(40)         not null,
   "branch_city"        VARCHAR2(20)         not null,
   "branch_property"    NUMBER               not null,
   constraint PK_SUBBRANCH primary key ("branch_name")
);

alter table "account"
   add constraint FK_ACCOUNT_ACCOUNT_I_STAFF foreign key ("staff_id")
      references "staff" ("staff_id");

alter table "borrow"
   add constraint FK_BORROW_BORROW_LOAN foreign key ("loan_id")
      references "loan" ("loan_id");

alter table "borrow"
   add constraint FK_BORROW_BORROW2_CLIENT foreign key ("client-_id")
      references "client" ("client-_id");

alter table "check_account"
   add constraint FK_CHECK_AC_ACCOUNT_T_ACCOUNT foreign key ("account_id")
      references "account" ("account_id");

alter table "client"
   add constraint FK_CLIENT_RELATION2_LINKMAN foreign key ("lin_client-_id")
      references "linkman" ("client-_id");

alter table "department"
   add constraint FK_DEPARTME_DEPT_SET_SUBBRANC foreign key ("branch_name")
      references "subbranch" ("branch_name");

alter table "linkman"
   add constraint FK_LINKMAN_RELATION_CLIENT foreign key ("client-_id")
      references "client" ("client-_id");

alter table "loan"
   add constraint FK_LOAN_RELATIONS_STAFF foreign key ("staff_id")
      references "staff" ("staff_id");

alter table "loan"
   add constraint FK_LOAN_PROVIDE_SUBBRANC foreign key ("branch_name")
      references "subbranch" ("branch_name");

alter table "loan_pay"
   add constraint FK_LOAN_PAY_LOAN_PAY_LOAN foreign key ("loan_id")
      references "loan" ("loan_id");

alter table "manager"
   add constraint FK_MANAGER_BELONG_STAFF foreign key ("staff_id")
      references "staff" ("staff_id");

alter table "open_account"
   add constraint FK_OPEN_ACC_OPEN_ACCO_ACCOUNT foreign key ("account_id")
      references "account" ("account_id");

alter table "open_account"
   add constraint FK_OPEN_ACC_OPEN_ACCO_CLIENT foreign key ("client-_id")
      references "client" ("client-_id");

alter table "saving_account"
   add constraint FK_SAVING_A_ACCOUNT_T_ACCOUNT foreign key ("account_id")
      references "account" ("account_id");

alter table "staff"
   add constraint FK_STAFF_HAVE_DEPARTME foreign key ("dept_id")
      references "department" ("dept_id");

alter table "staff"
   add constraint FK_STAFF_MANAGER_MANAGER foreign key ("man_staff_id")
      references "manager" ("staff_id");

