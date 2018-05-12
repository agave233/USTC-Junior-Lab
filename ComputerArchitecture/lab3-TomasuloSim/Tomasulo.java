
import java.awt.BorderLayout;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ItemEvent;
import java.awt.event.ItemListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.io.Reader;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.border.EtchedBorder;


public class Tomasulo extends JFrame implements ActionListener{

	private JPanel ins_set_panel,EX_time_set_panel,ins_state_panel,RS_panel,Load_panel,Registers_state_panel;


	private JButton stepbut,step5but,resetbut,startbut;

	private JComboBox inst_typebox[]=new JComboBox[24];


	private JLabel inst_typel, timel, tl1,tl2,tl3,tl4,resl,regl,ldl,insl,stepsl;
	private int time[]=new int[4];


	private JTextField tt1,tt2,tt3,tt4;

	private int intv[][]=new int[6][4], cnow, inst_typenow=0;
	private int cal[][]={{-1,0,0},{-1,0,0},{-1,0,0},{-1,0,0},{-1,0,0}};
	private int ld[][]={{0,0},{0,0},{0,0}};
	private int ff[]={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};


	private String  inst_type[]={"NOP","L.D","ADD.D","SUB.D","MULT.D","DIV.D"},
					regist_table[]={"F0","F2","F4","F6","F8","F10","F12","F14","F16"
							,"F18","F20","F22","F24","F26","F28","F30","F32"},
					rx[]={"R0","R1","R2","R3","R4","R5","R6"},
					ix[]={"0","1","2","3","4","5","6","7", "8","9","10",
                    "11","12","13","14","15","16","17","18","19","20","21",
                    "22","23","24","25","26","27","28","29","30","31"},
					rs_type[]={"Load1", "Load2", "Load3", "Add1","Add2","Add3","Mult1","Mult2"};

	private	String  my_inst_type[][]=new String[7][4], my_rs[][]=new String[6][8],
					my_load[][]=new String[4][4], my_regsters[][]=new String[3][17];
	private	JLabel  inst_typejl[][]=new JLabel[7][4], resjl[][]=new JLabel[6][8],
					ldjl[][]=new JLabel[4][4], regjl[][]=new JLabel[3][17];


	// class definition
	public class LoadStatus{
		public boolean busy;
		public int count_down;
		public int inst_index;
	}

	public class RsStations{
		public boolean busy;
		public int op;
		// public int vj;
		// public int vk;
		public int qj;
		public int qk;
		public int count_down;
		public int inst_index;
	}

	public  class RegStatus{
		public int state;
		public int value;
	}

	public class InstStatus{
		public boolean executing;
		public int rs_index;
	}

	private boolean rs_modified[] = new boolean[5];
	private int currentRegValue;
	private int instCount;
	private LoadStatus loadStats[] = new LoadStatus[3];
	private RegStatus regStats[] = new RegStatus[16];
	private RsStations rsStats[] = new RsStations[5];
	private InstStatus instStats[] = new InstStatus[6];

//构造方法
  public Tomasulo(){
	    super("Tomasulo Simulator");

	    //设置布局
	    Container cp=getContentPane();
	    FlowLayout layout=new FlowLayout();
	    cp.setLayout(layout);

	    //指令设置。GridLayout(int 指令条数, int 操作码+操作数, int hgap, int vgap)
	    inst_typel = new JLabel("指令设置");
	    ins_set_panel = new JPanel(new GridLayout(6,4,0,0));
	    ins_set_panel.setPreferredSize(new Dimension(350, 150));
	    ins_set_panel.setBorder(new EtchedBorder(EtchedBorder.RAISED));

	    //操作按钮:执行，重设，步进，步进5步
	    timel = new JLabel("执行时间设置");
	    EX_time_set_panel = new JPanel(new GridLayout(2,4,0,0));
	    EX_time_set_panel.setPreferredSize(new Dimension(280, 80));
	    EX_time_set_panel.setBorder(new EtchedBorder(EtchedBorder.RAISED));

	    //指令状态
	    insl = new JLabel("指令状态");
	    ins_state_panel = new JPanel(new GridLayout(7,4,0,0));
	    ins_state_panel.setPreferredSize(new Dimension(420, 175));
	    ins_state_panel.setBorder(new EtchedBorder(EtchedBorder.RAISED));


	    //寄存器状态
	    regl = new JLabel("寄存器");
	    Registers_state_panel = new JPanel(new GridLayout(3,17,0,0));
	    Registers_state_panel.setPreferredSize(new Dimension(740, 75));
	    Registers_state_panel.setBorder(new EtchedBorder(EtchedBorder.RAISED));
	    //保留站
	    resl = new JLabel("保留站");
	    RS_panel = new JPanel(new GridLayout(6,7,0,0));
	    RS_panel.setPreferredSize(new Dimension(630, 150));
	    RS_panel.setBorder(new EtchedBorder(EtchedBorder.RAISED));
	    //Load部件
	    ldl = new JLabel("Load部件");
	    Load_panel = new JPanel(new GridLayout(4,4,0,0));
	    Load_panel.setPreferredSize(new Dimension(300, 100));
	    Load_panel.setBorder(new EtchedBorder(EtchedBorder.RAISED));

	    tl1 = new JLabel("Load");
	    tl2 = new JLabel("加/减");
	    tl3 = new JLabel("乘法");
	    tl4 = new JLabel("除法");

		stepsl = new JLabel();
		stepsl.setPreferredSize(new Dimension(200, 30));
		stepsl.setHorizontalAlignment(SwingConstants.CENTER);
		stepsl.setBorder(new EtchedBorder(EtchedBorder.RAISED));
	    stepbut = new JButton("步进");
	    stepbut.addActionListener(this);
	    step5but = new JButton("步进5步");
	    step5but.addActionListener(this);
	    startbut = new JButton("执行");
	    startbut.addActionListener(this);
	    resetbut= new JButton("重设");
	    resetbut.addActionListener(this);
		tt1 = new JTextField("2");
		tt2 = new JTextField("2");
		tt3 = new JTextField("10");
		tt4 = new JTextField("40");

		for (int i=0;i<2;i++)
			for (int j=0;j<4;j++){
				if (j==0){
					inst_typebox[i*4+j]=new JComboBox(inst_type);
				}
				else if (j==1){
					inst_typebox[i*4+j]=new JComboBox(regist_table);
				}
				else if (j==2){
					inst_typebox[i*4+j]=new JComboBox(ix);
				}
				else {
					inst_typebox[i*4+j]=new JComboBox(rx);
				}
				inst_typebox[i*4+j].addActionListener(this);
				ins_set_panel.add(inst_typebox[i*4+j]);
			}
		for (int i=2;i<6;i++)
			for (int j=0;j<4;j++){
				if (j==0){
					inst_typebox[i*4+j]=new JComboBox(inst_type);
				}
				else {
					inst_typebox[i*4+j]=new JComboBox(regist_table);
				}
				inst_typebox[i*4+j].addActionListener(this);
				ins_set_panel.add(inst_typebox[i*4+j]);
			}

		inst_typebox[0].setSelectedIndex(1);
		inst_typebox[1].setSelectedIndex(3);
		inst_typebox[2].setSelectedIndex(21);
		inst_typebox[3].setSelectedIndex(2);

		inst_typebox[4].setSelectedIndex(1);
		inst_typebox[5].setSelectedIndex(1);
		inst_typebox[6].setSelectedIndex(20);
		inst_typebox[7].setSelectedIndex(3);

		inst_typebox[8].setSelectedIndex(4);
		inst_typebox[9].setSelectedIndex(0);
		inst_typebox[10].setSelectedIndex(1);
		inst_typebox[11].setSelectedIndex(2);

		inst_typebox[12].setSelectedIndex(3);
		inst_typebox[13].setSelectedIndex(4);
		inst_typebox[14].setSelectedIndex(3);
		inst_typebox[15].setSelectedIndex(1);

		inst_typebox[16].setSelectedIndex(5);
		inst_typebox[17].setSelectedIndex(5);
		inst_typebox[18].setSelectedIndex(0);
		inst_typebox[19].setSelectedIndex(3);

		inst_typebox[20].setSelectedIndex(2);
		inst_typebox[21].setSelectedIndex(3);
		inst_typebox[22].setSelectedIndex(4);
		inst_typebox[23].setSelectedIndex(1);
		
		// inst_typebox[0].setSelectedIndex(1);
		// inst_typebox[1].setSelectedIndex(4);
		// inst_typebox[2].setSelectedIndex(21);
		// inst_typebox[3].setSelectedIndex(2);

		// inst_typebox[4].setSelectedIndex(1);
		// inst_typebox[5].setSelectedIndex(2);
		// inst_typebox[6].setSelectedIndex(16);
		// inst_typebox[7].setSelectedIndex(3);

		// inst_typebox[8].setSelectedIndex(4);
		// inst_typebox[9].setSelectedIndex(1);
		// inst_typebox[10].setSelectedIndex(2);
		// inst_typebox[11].setSelectedIndex(3);

		// inst_typebox[12].setSelectedIndex(3);
		// inst_typebox[13].setSelectedIndex(5);
		// inst_typebox[14].setSelectedIndex(4);
		// inst_typebox[15].setSelectedIndex(2);

		// inst_typebox[16].setSelectedIndex(5);
		// inst_typebox[17].setSelectedIndex(6);
		// inst_typebox[18].setSelectedIndex(1);
		// inst_typebox[19].setSelectedIndex(4);

		// inst_typebox[20].setSelectedIndex(2);
		// inst_typebox[21].setSelectedIndex(4);
		// inst_typebox[22].setSelectedIndex(5);
		// inst_typebox[23].setSelectedIndex(2);

		EX_time_set_panel.add(tl1);
		EX_time_set_panel.add(tt1);
		EX_time_set_panel.add(tl2);
		EX_time_set_panel.add(tt2);
		EX_time_set_panel.add(tl3);
		EX_time_set_panel.add(tt3);
		EX_time_set_panel.add(tl4);
		EX_time_set_panel.add(tt4);

		for (int i=0;i<7;i++)
		{
			for (int j=0;j<4;j++){
				inst_typejl[i][j]=new JLabel(my_inst_type[i][j]);
				inst_typejl[i][j].setBorder(new EtchedBorder(EtchedBorder.RAISED));
				ins_state_panel.add(inst_typejl[i][j]);
			}
		}

		for (int i=0;i<6;i++)
		{
			for (int j=0;j<8;j++){
				resjl[i][j]=new JLabel(my_rs[i][j]);
				resjl[i][j].setBorder(new EtchedBorder(EtchedBorder.RAISED));
				RS_panel.add(resjl[i][j]);
			}
		}

		for (int i=0;i<4;i++)
		{
			for (int j=0;j<4;j++){
				ldjl[i][j]=new JLabel(my_load[i][j]);
				ldjl[i][j].setBorder(new EtchedBorder(EtchedBorder.RAISED));
				Load_panel.add(ldjl[i][j]);
			}
		}

		for (int i=0;i<3;i++)
		{
			for (int j=0;j<17;j++){
				regjl[i][j]=new JLabel(my_regsters[i][j]);
				regjl[i][j].setBorder(new EtchedBorder(EtchedBorder.RAISED));
				Registers_state_panel.add(regjl[i][j]);
			}
		}


		cp.add(inst_typel);
		cp.add(ins_set_panel);
		cp.add(timel);
		cp.add(EX_time_set_panel);

		cp.add(startbut);
		cp.add(resetbut);
		cp.add(stepbut);
		cp.add(step5but);

		cp.add(Load_panel);
		cp.add(ldl);
		cp.add(RS_panel);
		cp.add(resl);
		cp.add(stepsl);
		cp.add(Registers_state_panel);
		cp.add(regl);
		cp.add(ins_state_panel);
		cp.add(insl);

		stepbut.setEnabled(false);
		step5but.setEnabled(false);
		ins_state_panel.setVisible(false);
		insl.setVisible(false);
		RS_panel.setVisible(false);
		ldl.setVisible(false);
		Load_panel.setVisible(false);
		resl.setVisible(false);
		stepsl.setVisible(false);
		Registers_state_panel.setVisible(false);
		regl.setVisible(false);
		setSize(820,620);
		setVisible(true);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	}


	public void init(){
		// get value
		// handl NOP inst !!!
		int k = 0;
		for (int i=0;i<6;i++){
			int instType=inst_typebox[i*4].getSelectedIndex();
			if (instType!=0){
				intv[k][0]=instType;
				intv[k][1]=inst_typebox[i*4+1].getSelectedIndex();
				if (intv[k][0]==1){
					intv[k][2]=inst_typebox[i*4+2].getSelectedIndex();
					intv[k][3]=inst_typebox[i*4+3].getSelectedIndex();
				}
				else {
					intv[k][2]=inst_typebox[i*4+2].getSelectedIndex();
					intv[k][3]=inst_typebox[i*4+3].getSelectedIndex();
				}
				k++;
			}
		}
		time[0]=Integer.parseInt(tt1.getText());
		time[1]=Integer.parseInt(tt2.getText());
		time[2]=Integer.parseInt(tt3.getText());
		time[3]=Integer.parseInt(tt4.getText());
		//System.out.println(time[0]);
		// set 0
		my_inst_type[0][0]="指令";
		my_inst_type[0][1]="流出";
		my_inst_type[0][2]="执行";
		my_inst_type[0][3]="写回";


		my_load[0][0]="名称";
		my_load[0][1]="Busy";
		my_load[0][2]="地址";
		my_load[0][3]="值";
		my_load[1][0]="Load1";
		my_load[2][0]="Load2";
		my_load[3][0]="Load3";
		my_load[1][1]="no";
		my_load[2][1]="no";
		my_load[3][1]="no";

		my_rs[0][0]="Time";
		my_rs[0][1]="名称";
		my_rs[0][2]="Busy";
		my_rs[0][3]="Op";
		my_rs[0][4]="Vj";
		my_rs[0][5]="Vk";
		my_rs[0][6]="Qj";
		my_rs[0][7]="Qk";
		my_rs[1][1]="Add1";
		my_rs[2][1]="Add2";
		my_rs[3][1]="Add3";
		my_rs[4][1]="Mult1";
		my_rs[5][1]="Mult2";
		my_rs[1][2]="no";
		my_rs[2][2]="no";
		my_rs[3][2]="no";
		my_rs[4][2]="no";
		my_rs[5][2]="no";

		my_regsters[0][0]="字段";
		for (int i=1;i<17;i++){
			//System.out.print(i+" "+regist_table[i-1];
			my_regsters[0][i]=regist_table[i-1];

		}
		my_regsters[1][0]="状态";
		my_regsters[2][0]="值";

		for (int i=1,m=1;i<7;i++)
		for (int j=0;j<4;j++){
			if (j==0){
				int temp=i-1;
				String disp;
				disp = inst_type[inst_typebox[temp*4].getSelectedIndex()]+" ";
				if (inst_typebox[temp*4].getSelectedIndex()==0) continue;
				else if (inst_typebox[temp*4].getSelectedIndex()==1){
					disp=disp+regist_table[inst_typebox[temp*4+1].getSelectedIndex()]+','+ix[inst_typebox[temp*4+2].getSelectedIndex()]+'('+rx[inst_typebox[temp*4+3].getSelectedIndex()]+')';
				}
				else {
					disp=disp+regist_table[inst_typebox[temp*4+1].getSelectedIndex()]+','+regist_table[inst_typebox[temp*4+2].getSelectedIndex()]+','+regist_table[inst_typebox[temp*4+3].getSelectedIndex()];
				}
				my_inst_type[m][j]=disp;
				m++;
			}
			else my_inst_type[i][j]="";
		}
		for (int i=1;i<6;i++)
		for (int j=0;j<8;j++)if (j!=1&&j!=2){
			my_rs[i][j]="";
		}
		for (int i=1;i<4;i++)
		for (int j=2;j<4;j++){
			my_load[i][j]="";
		}
		for (int i=1;i<3;i++)
		for (int j=1;j<17;j++){
			my_regsters[i][j]="";
		}

		// for (int i=0;i<5;i++){
		// 	for (int j=1;j<3;j++) cal[i][j]=0;
		// 	cal[i][0]=-1;
		// }
		// for (int i=0;i<3;i++)
		// 	for (int j=0;j<2;j++) ld[i][j]=0;
		// for (int i=0;i<17;i++) ff[i]=0;

		inst_typenow = 0;
		instCount = k;
		currentRegValue = 1;
		for(int i = 0;i < 3;i++){
			loadStats[i] = new LoadStatus();
			loadStats[i].busy = false;
			loadStats[i].inst_index = -1;
			loadStats[i].count_down = -1;
		}
		for(int i = 0;i < 5;i++){
			rsStats[i] = new RsStations();
			rsStats[i].busy = false;
			rsStats[i].count_down = -1;
			rsStats[i].qj = -1;
			rsStats[i].qk = -1;
		}
		for(int i = 0;i < 16;i++){
			regStats[i] = new RegStatus();
			regStats[i].state = -1;
			regStats[i].value = 0;
		}
		for(int i = 0;i < 6;i++){
			instStats[i] = new InstStatus();
			instStats[i].executing = false;
			instStats[i].rs_index = -1;
		}
	}

	public void display(){
		for (int i=0;i<7;i++)
			for (int j=0;j<4;j++){
				inst_typejl[i][j].setText(my_inst_type[i][j]);
			}
		for (int i=0;i<6;i++)
			for (int j=0;j<8;j++){
				resjl[i][j].setText(my_rs[i][j]);
			}
		for (int i=0;i<4;i++)
			for (int j=0;j<4;j++){
				ldjl[i][j].setText(my_load[i][j]);
			}
		for (int i=0;i<3;i++)
			for (int j=0;j<17;j++){
				regjl[i][j].setText(my_regsters[i][j]);
			}
		stepsl.setText("当前周期："+String.valueOf(cnow-1));
	}

	public void actionPerformed(ActionEvent e){

		if (e.getSource()==startbut) {
			for (int i=0;i<24;i++) inst_typebox[i].setEnabled(false);
			tt1.setEnabled(false);tt2.setEnabled(false);
			tt3.setEnabled(false);tt4.setEnabled(false);
			stepbut.setEnabled(true);
			step5but.setEnabled(true);
			startbut.setEnabled(false);

			init();
			cnow=1;

			display();
			ins_state_panel.setVisible(true);
			RS_panel.setVisible(true);
			Load_panel.setVisible(true);
			Registers_state_panel.setVisible(true);
			insl.setVisible(true);
			ldl.setVisible(true);
			resl.setVisible(true);
			stepsl.setVisible(true);
			regl.setVisible(true);
		}

		if (e.getSource()==resetbut) {
			for (int i=0;i<24;i++) inst_typebox[i].setEnabled(true);
			tt1.setEnabled(true);tt2.setEnabled(true);
			tt3.setEnabled(true);tt4.setEnabled(true);
			stepbut.setEnabled(false);
			step5but.setEnabled(false);
			startbut.setEnabled(true);
			ins_state_panel.setVisible(false);
			insl.setVisible(false);
			RS_panel.setVisible(false);
			ldl.setVisible(false);
			Load_panel.setVisible(false);
			resl.setVisible(false);
			stepsl.setVisible(false);
			Registers_state_panel.setVisible(false);
			regl.setVisible(false);
		}

		if (e.getSource()==stepbut) {
			core();
			cnow++;
			display();
		}

		if (e.getSource()==step5but) {
			for (int i=0;i<5;i++){
				core();
				cnow++;
			}
			display();
		}

		for (int i=0;i<24;i=i+4)
		{
			if (e.getSource()==inst_typebox[i]) {
				if (inst_typebox[i].getSelectedIndex()==1){
					inst_typebox[i+2].removeAllItems();
					for (int j=0;j<ix.length;j++) inst_typebox[i+2].addItem(ix[j]);
					inst_typebox[i+3].removeAllItems();
					for (int j=0;j<rx.length;j++) inst_typebox[i+3].addItem(rx[j]);
				}
				else {
					inst_typebox[i+2].removeAllItems();
					for (int j=0;j<regist_table.length;j++) inst_typebox[i+2].addItem(regist_table[j]);
					inst_typebox[i+3].removeAllItems();
					for (int j=0;j<regist_table.length;j++) inst_typebox[i+3].addItem(regist_table[j]);
				}
			}
		}
	}


	public void loadInst_write(int i){
		int inst_index = loadStats[i].inst_index;
		int rd_index = intv[inst_index][1];

		if(loadStats[i].count_down == 0 && loadStats[i].busy){
			loadStats[i].busy = false;
			loadStats[i].inst_index = -1;
			my_load[i + 1][1] = "no";
			my_load[i + 1][2] = "";
			my_load[i + 1][3] = "";

			my_inst_type[inst_index + 1][3] = Integer.toString(cnow);

			// update qj/qk of rsStats.
			for(int j = 0;j < 5;j++){
				if(rsStats[j].busy == false)
					continue;
				if(rsStats[j].qj == i){
					rsStats[j].qj = -1;
					my_rs[j + 1][4] = "M" + Integer.toString(currentRegValue);
					my_rs[j + 1][6] = "";
					rs_modified[j] = true;
				}
				if(rsStats[j].qk == i){
					rsStats[j].qk = -1;
					my_rs[j + 1][5] = "M" + Integer.toString(currentRegValue);
					my_rs[j + 1][7] = "";
					rs_modified[j] = true;
				}
			} 
			// issue stage can appply this state !!!
			regStats[rd_index].state = -1;
			regStats[rd_index].value = currentRegValue;
			// my_regsters[1][rd_index + 1] = "";
			my_regsters[2][rd_index + 1] = "M" + Integer.toString(currentRegValue);
			currentRegValue++;

		}

	}

	public void fpInst_Write(int i){
		int inst_index = rsStats[i].inst_index;
		int rd_index = intv[inst_index][1];

		if(rsStats[i].count_down == 0 && rsStats[i].busy){
			rsStats[i].busy = false;
			rsStats[i].count_down = -1;
			rsStats[i].inst_index = -1;
			rsStats[i].qj = -1;
			rsStats[i].qk = -1;

			my_inst_type[inst_index + 1][3] = Integer.toString(cnow);

			my_rs[i + 1][2] = "no";
			for(int j = 3;j < 6;j++)
				my_rs[i + 1][j] = "";

			// update qj/qk of rsStats.
			for(int j = 0;j < 5;j++){
				if(rsStats[j].busy == false)
					continue;
				if(rsStats[j].qj == i + 3){
					rsStats[j].qj = -1;
					my_rs[j + 1][4] = "M" + Integer.toString(currentRegValue);
					my_rs[j + 1][6] = "";
					rs_modified[j] = true;
				}
				if(rsStats[j].qk == i + 3){
					rsStats[j].qk = -1;
					my_rs[j + 1][5] = "M" + Integer.toString(currentRegValue);
					my_rs[j + 1][7] = "";
					rs_modified[j] = true;
				}
			} 
			// issue stage can appply this state !!!
			regStats[rd_index].state = -1;
			regStats[rd_index].value = currentRegValue;
			// my_regsters[1][rd_index + 1] = "";
			my_regsters[2][rd_index + 1] = "M" + Integer.toString(currentRegValue);
			currentRegValue++;

		}

	}

	public void core()
	{
		
		/* 
			Write result stage
			update rsStasts, instStats, regStats,
			clear loadStats for ld insts.
			clear rsStats for fp insts.
		*/
		// 1.wb阶段可能会对ex端造成影响，标记一下。
		// 2.修改框架代码，使得支持插入nop指令以及显示
      for (int i = 0;i < 5;i++) rs_modified[i] = false;

		for(int i = 0;i < 6;i++){
			int rs_index = instStats[i].rs_index;
			if(instStats[i].executing){
				if(rs_index < 3)
					loadInst_write(rs_index);
				else
					fpInst_Write(rs_index - 3);
				instStats[i].executing = false;
			}
		}

		// for(int i = 0;i < 3;i++){
		// }
		// for(int i = 0;i < 5;i++){
		// }

		/* 
			Execute stage
			update rsStasts, instStats, regStats,
		*/
		// Execute for LD insts.
		for(int i = 0;i < 3;i++){
			if(loadStats[i].busy && loadStats[i].count_down > 0){
				int inst_index = loadStats[i].inst_index; 
				instStats[inst_index].executing = true;
				// Start executing.
				if(loadStats[i].count_down == time[0]){
					int rs_index = intv[inst_index][3];
					my_inst_type[inst_index + 1][2] = Integer.toString(cnow) + "~";
					my_load[i + 1][2] += "+(" + rx[rs_index] + ")";
				}
				// finish loading.
				if(loadStats[i].count_down == 1){
					my_inst_type[inst_index + 1][2] += Integer.toString(cnow);
					my_load[i + 1][3] = "M[" + my_load[i + 1][2] + "]";
				}
				loadStats[i].count_down--;
			}
		}
		// Execute for FP insts.
		for(int i = 0;i < 5;i++){
			int inst_index = rsStats[i].inst_index; 
			// int issue_type = intv[i][0];
			// int rd = intv[i][1];
			// int rs = intv[i][2];
			// int rt = intv[i][3];
			if(rsStats[i].busy){

				// No conflict, can exexcute.
				if(rsStats[i].qj == -1 && rsStats[i].qk == -1 && !rs_modified[i]){
					instStats[inst_index].executing = true;
					// start computing.
					if((rsStats[i].count_down == time[1] && rsStats[i].op < 4) ||
					   (rsStats[i].count_down == time[2] && rsStats[i].op == 4) ||
					   (rsStats[i].count_down == time[3] && rsStats[i].op == 5)){
						my_inst_type[inst_index + 1][2] = Integer.toString(cnow) + "~";
					}
						
					// finish compution
					if(rsStats[i].count_down == 1)
						my_inst_type[inst_index + 1][2] += Integer.toString(cnow);
					rsStats[i].count_down--;
					// update RS table.
					if(rsStats[i].count_down > 0)
						my_rs[i + 1][0] = Integer.toString(rsStats[i].count_down);
					else
						my_rs[i + 1][0] = "";
				}
			}	
		}
	
		/* 
			Issue stage
			update rsStasts, instStats, regStats,
		*/
		if(inst_typenow < instCount){
			int issue_type = intv[inst_typenow][0];
			int rd = intv[inst_typenow][1];

			// LD inst, update (no rsStats), regStats, loadStats.
			if(issue_type == 1){
				int offset = intv[inst_typenow][2];
				int rs = intv[inst_typenow][3];
				int load_index;

				// find an empty load.
				for(load_index = 0;load_index < 3;load_index++)
					if(!loadStats[load_index].busy)
						break;

				// can issue this inst.
				if(load_index < 3){
					loadStats[load_index].busy = true;
					loadStats[load_index].inst_index = inst_typenow;
					loadStats[load_index].count_down = time[0];

					// rs Reg is not ready, and need to wait..emmm, it doesnot happen.
					// update regStats and reg table.
					regStats[rd].state = load_index;
					my_regsters[1][rd + 1] = rs_type[load_index];
					// update load table.
					my_load[load_index + 1][1] = "yes"; 
					my_load[load_index + 1][2] = Integer.toString(offset);
					// update inst table.
					my_inst_type[inst_typenow + 1][1] = Integer.toString(cnow);
					instStats[inst_typenow].rs_index = load_index;
				}

			}

			// BNEZ inst, 
			else if(issue_type == 6){

			}

			// FP inst, update rsStats, regStats, inst table, RS table, reg table.
			else if(issue_type != 0){
				int rs = intv[inst_typenow][2];
				int rt = intv[inst_typenow][3];
				int fp_index;

				if(issue_type < 4){
					for(fp_index = 0;fp_index < 3;fp_index++)
						if(!rsStats[fp_index].busy)
							break;
				}
				else{
					for(fp_index = 3;fp_index < 5;fp_index++)
						if(!rsStats[fp_index].busy)
							break;					
				}



				// can issue add/sub or mul/div inst.
				if((fp_index < 3 && issue_type < 4) ||
				   (fp_index < 5 && fp_index >= 3 && issue_type >= 4)){


				   	rsStats[fp_index].inst_index = inst_typenow; 
				   	rsStats[fp_index].busy = true;
				   	rsStats[fp_index].op = issue_type;
				   	if(issue_type < 4)
						rsStats[fp_index].count_down = time[1];
					if(issue_type == 4)
						rsStats[fp_index].count_down = time[2];
					if(issue_type == 5)
						rsStats[fp_index].count_down = time[3];

					// check RAW for rs and rt, update rsStats and RS table.
					my_rs[fp_index + 1][2] = "yes";
					my_rs[fp_index + 1][3] = inst_type[issue_type];
					if(regStats[rs].state != -1){
						rsStats[fp_index].qj = regStats[rs].state;	
						my_rs[fp_index + 1][6] = rs_type[regStats[rs].state];
					}
					else{
						rsStats[fp_index].qj = -1;
						if(regStats[rs].value == 0)
							my_rs[fp_index + 1][4] = regist_table[rs];
						else
							my_rs[fp_index + 1][4] = 'M' + Integer.toString(regStats[rs].value);

					}
					if(regStats[rt].state != -1){
						rsStats[fp_index].qk = regStats[rt].state;	
						my_rs[fp_index + 1][7] = rs_type[regStats[rt].state];
					}
					else{
						rsStats[fp_index].qk = -1;
						if(regStats[rt].value == 0)
							my_rs[fp_index + 1][5] = regist_table[rt];
						else
							my_rs[fp_index + 1][5] = 'M' + Integer.toString(regStats[rt].value);
					}	

					// update regStats and reg table.
					regStats[rd].state = fp_index + 3;
					my_regsters[1][rd + 1] = rs_type[fp_index + 3];	
					// update inst table.
					my_inst_type[inst_typenow + 1][1] = Integer.toString(cnow);
					instStats[inst_typenow].rs_index = fp_index + 3;
				}

			}

			inst_typenow++;
		} 

	}

	public static void main(String[] args) {
		new Tomasulo();
	}

}
