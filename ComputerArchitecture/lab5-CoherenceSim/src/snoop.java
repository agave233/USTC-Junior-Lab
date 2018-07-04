import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer; 
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
public class snoop {	
	/*****创建panel2~panel5******/
	// static Mypanel panel2 =new Mypanel(0);
	// static Mypanel panel3 =new Mypanel(1);
	// static Mypanel panel4 =new Mypanel(2);
	// static Mypanel panel5 =new Mypanel(3);

	/*********memory的标题*********/
	static String[] Mem_ca={
			"Memory0","Memory1","Memory2"
	};
	
	/*********memory中的内容*********/
	static String[][] Mem_Content ={
			{"0","10","20"},{"1","11","21"},{"2","12","22"},
			{"3","13","23"},{"4","14","24"},{"5","15","25"},
			{"6","16","26"},{"7","17","27"},{"8","18","28"},
			{"9","19","29"}
	};
	static Mypanel[] panel = new Mypanel[4];
	static JTable table_2 = new JTable(Mem_Content,Mem_ca); 
	static JLabel info_label = new JLabel("结果/过程:"); 

	static JComboBox<String> Mylistmodel1_1 = new JComboBox<>(new Mylistmodel());
	static class Mylistmodel extends AbstractListModel<String> implements ComboBoxModel<String>{		
		private static final long serialVersionUID = 1L;
		String selecteditem="直接映射";
		private String[] test={"直接映射","两路组相联","四路组相联"};
		public String getElementAt(int index){
			return test[index];
		}
		public int getSize(){
			return test.length;
		}
		public void setSelectedItem(Object item){
			selecteditem=(String)item;
		}
		public Object getSelectedItem( ){
			return selecteditem;
		}
		public int getIndex() {
			for (int i = 0; i < test.length; i++) {
				if (test[i].equals(getSelectedItem()))
					return i;
			}
			return 0;
		}
		
	}
	static class Mylistmodel2 extends AbstractListModel<String> implements ComboBoxModel<String>{		
		private static final long serialVersionUID = 1L;
		String selecteditem=null;
		private String[] test={"读","写"};
		public String getElementAt(int index){
			return test[index];
		}
		public int getSize(){
			return test.length;
		}
		public void setSelectedItem(Object item){
			selecteditem=(String)item;
		}
		public Object getSelectedItem( ){
			return selecteditem;
		}
		public int getIndex() {
			for (int i = 0; i < test.length; i++) {
				if (test[i].equals(getSelectedItem()))
					return i;
			}
			return 0;
		}
		
	}
	
	static class Mypanel extends JPanel implements ActionListener {
		private static final long serialVersionUID = 1L;
		JLabel label=new JLabel("访问地址");
		JLabel label_2=new JLabel("Process1");
		
		JTextField jtext=new JTextField("");
		JButton button=new JButton("执行");
		JComboBox<String> Mylistmodel = new JComboBox<>(new Mylistmodel2());
		
		int id;
		Color Gray = new Color(192, 192, 192);
		private int[] cache_addr = {-1, -1, -1, -1};
		private Color[] color = {Gray, Gray, Gray, Gray};
		private String[] cache_op = {"", "", "", ""};
		private String[] cache_state = {"I", "I", "I", "I"};

		/*********cache中的标题*********/
		String[] Cache_ca={"Cache","读/写","目标地址"};
		/*********cache中的内容*********/
		String[][] Cache_Content = {
				{"0"," "," "},{"1"," "," "},{"2"," "," "},{"3"," "," "}
		};
		/************cache的滚动模版***********/
		JTable table_1 = new JTable(Cache_Content,Cache_ca); 
		JScrollPane scrollPane = new JScrollPane(table_1);
		/*
		/************memory的滚动模版**********
		JTable table_2 = new JTable(Mem_Content,Mem_ca); 
		JScrollPane scrollPane2 = new JScrollPane(table_2);
		*/
		public Mypanel(int k){
			super();
			id = k;
			setSize(350, 250);
			setLayout(null);
			
			/*****添加原件********/
			add(jtext);
			add(label);
			add(label_2);
			add(button);
			add(Mylistmodel);
			add(scrollPane);
			//add(scrollPane2);
			
			/****设置原件大小与字体********/
			label_2.setFont(new Font("华文楷体",0,16));
			label_2.setBounds(10, 10, 100, 30);
			
			label.setFont(new Font("华文楷体",0,16));
			label.setBounds(10, 50, 100, 30);
			
			jtext.setFont(new Font("华文楷体",0,15));
			jtext.setBounds(100, 50, 50, 30);

			table_1.getTableHeader().setFont(new Font("华文楷体",0,15));
			table_1.setFont(new Font("华文楷体",0,15));
			
			Mylistmodel.setSelectedItem("读");
			Mylistmodel.setFont(new Font("华文楷体",0,15));
			Mylistmodel.setBounds(160, 50, 50, 30);
			
			scrollPane.setFont(new Font("华文楷体",0,15));
			scrollPane.setBounds(10, 90, 310, 90);
			
			//scrollPane2.setFont(new Font("华文楷体",1,15));
			//scrollPane2.setBounds(10, 190, 310, 180);
			
			button.setFont(new Font("华文楷体",0,15));
			button.setBounds(220,50, 100, 35);
			
			/******添加按钮事件********/
			button.addActionListener(this);
			this.setColor(table_1, color);
		}
		
		public void init(){
			/******Mypanel的初始化******/
			jtext.setText("");
			Mylistmodel.setSelectedItem("读");
			for(int i=0;i<=3;i++)
				for(int j=1;j<=2;j++)
					Cache_Content[i][j]=" ";
			for(int i=0;i<=9;i++)
				for(int j=1;j<=2;j++)
					Mem_Content[i][j]=" ";

			for(int i = 0;i < 4;i++){
				cache_addr[i] = -1;
				cache_op[i] = "";
				cache_state[i] = "I";
			}

			this.show_cache();
			setVisible(false);
			setVisible(true);
			
		}

		// color
		public static void setColor(JTable table,Color[] color) {
		        try {
		            DefaultTableCellRenderer dtcr = new DefaultTableCellRenderer() {
		            	@Override
		            	public Component getTableCellRendererComponent(JTable table,Object value, boolean isSelected, boolean hasFocus,int row, int column) {
		            		setBackground(color[row]);
		            		setForeground(Color.WHITE);
		            		return super.getTableCellRendererComponent(table, value,isSelected, hasFocus, row, column);
		            	}
		            };
		            // 对每行的每一个单元格
		            int columnCount = table.getColumnCount();
		            for (int i = 0; i < columnCount; i++) {
		                table.getColumn(table.getColumnName(i)).setCellRenderer(dtcr);
		            }

		        } catch (Exception e) {
		            e.printStackTrace();
		        }
		    }		


			public void simulate_cache(){

			String addr_text = this.jtext.getText();
			if(addr_text == "")
				return;
			String info = "<html><body>结果/过程:<br>";
			int i, index0 = -1, index = -1, k = 1;
			int addr = Integer.parseInt(addr_text);
			int type = Mylistmodel1_1.getSelectedIndex();
			int op = this.Mylistmodel.getSelectedIndex();

			if(addr > 29){
				System.out.println("输入地址错误，应小于30");
				info += "输入地址错误，应小于30</body></html>";
				info_label.setText(info);
				return;
			}

			// result: hit
			for(i = 0;i < 4;i++)
				if(cache_addr[i] == addr && cache_state[i] != "I"){
					String s = "在处理器" + Integer.toString(this.id + 1)
					 + "中命中内存地址" + Integer.toString(addr);
					 System.out.println(s);
					 info += k++ + s + "<br>";
					index = i;
					break;
				}

			// result: miss
			if(i == 4){
				String s = "在处理器" + Integer.toString(this.id + 1)
				 + "中未命中内存地址" + Integer.toString(addr);
				 System.out.println(s);
				 info += k++ + s + "<br>";	
				if(type == 0){
					index0 = addr % 4;
					if(cache_state[index0] == "I")
						index = index0;
				}
				if(type == 1){
					index0 = 2 * (addr % 2);
					if(cache_state[index0] == "I")
						index = index0;
					else if(cache_state[index0 + 1] == "I")
						index = index0 + 1;
				}
				if(type == 2){
					index0 = 0;
					for(i = 0;i < 4;i++)
						if(cache_state[i] == "I"){
							index = i;
							break;
						}
				}
				// action: replace 
				if(index == -1){
					index = index0;
					if(cache_state[index] == "S"){
						// do nothing
						s = "将Cache中的" + Integer.toString(this.cache_addr[index]) + "替换为" + Integer.toString(addr);
						System.out.println(s);
						info += k++ + s + "<br>";
					}
					if(cache_state[index] == "M"){
						s = "将处理器" +  Integer.toString(this.id + 1) + "Cache中的第"
						 + Integer.toString(index + 1) + "块写回到主存储器中地址为" + Integer.toString(addr) + "的区域";
						 System.out.println(s);
						 info += k++ + s + "<br>";
					}
					// state: S->I or M -> I
					cache_state[index] = "I";
				}	
				cache_addr[index] = addr;		
			}

			// action: Process Read
			if(op == 0){
				if(index0 == -1){
					// state: M or S
					String s = "直接从Cahce中读取数据到CPU";
					System.out.println(s);
					info += k++ + s + "<br>";
				}
				else{
					// state: I -> S
					boolean found_ex = false;
					for(i = 0;i < 4;i++){
						if(this.id == i)
							continue;
						for(int j = 0;j < 4;j++){
							if(panel[i].cache_addr[j] == addr && panel[i].cache_state[j] == "M"){
								// Observe: BusRd
								// action: flush
								// state: M -> S
								String s1 = "在处理器" + Integer.toString(i + 1) + "Cache中独享该块,通过总线写回存储器";
								String s2 = "传块优化：直接在总线上从" + Integer.toString(i + 1) + "的Cache中传送到当前Cache中";
								System.out.println(s1);
								System.out.println(s2);
								info += k++ + s2 + "<br>" + s1 + "<br>";
								panel[i].cache_state[j] = "S";		
								found_ex = true;
								break;				
							}

						}
						if(found_ex)
							break;
					}
					if(found_ex == false){				
						String s = "从存储器中读取数据到Cache中，然后从Cache中读取数据到CPU";
						System.out.println(s);
						info += k++ + s + "<br>";						
					}
					this.cache_state[index] = "S";
				}
				this.cache_op[index] = "读";
			}

			// action: Process Write
			if(op == 1){
				boolean bus_rdx = false;
				if(this.cache_state[index] == "M"){
					// state: M -> M
					String s = "Cache中的独享块重新被写入数据";
					System.out.println(s);
					info += k++ + s + "<br>";					
				}
				if(this.cache_state[index] == "S"){
					// state: S -> M
					// signal: BusRdX
					this.cache_state[index] = "M";
					bus_rdx = true;
				}
				if(this.cache_state[index] == "I"){
					// state: I -> M
					// signal: BusRdX
					this.cache_state[index] = "M";
					bus_rdx = true;
				}
				// Observe: BusRdX
				if(bus_rdx){
					for(i = 0;i < 4;i++){
						if(this.id == i)
							continue;
						for(int j = 0;j < 4;j++){
							if(panel[i].cache_addr[j] == addr && panel[i].cache_state[j] == "M"){
								String s1 = "在处理器" + Integer.toString(i + 1) + "Cache中独享该块,要通过总线写回存储器";
								String s2 = "传块优化：直接在总线上从" + Integer.toString(i + 1) + "的Cache中传送到当前Cache中";
								System.out.println(s1);
								System.out.println(s2);
								info += k++ + s1 + "<br>" + s2 + "<br>";
								panel[i].cache_state[j] = "I";
								break;										
							}
							if(panel[i].cache_addr[j] == addr && panel[i].cache_state[j] == "S"){
								String s = "在处理器" + Integer.toString(i + 1) + "Cache中共享该块,写作废";
								System.out.println(s);
								info += k++ + s + "<br>";
								panel[i].cache_state[j] = "I";
							}	
						}		
					}
					String s = "Cache内的新块被写入数据，变为独享块";
					System.out.println(s);
					info += k++ + s + "<br>";					
				}

				this.cache_op[index] = "写";
			}

			info += "</body></html>";
			info_label.setText(info);
			for(i = 0;i < 3;i++){
				if(i == addr / 10)
					memsetColor(table_2, addr % 10, addr / 10, new Color(205, 85, 85));
				else
					memsetColor(table_2, 0, i, new Color(255,222,173));
			}
			table_2.updateUI();

		}

		public void show_cache(){
			for(int i = 0;i < 4;i++){
				if(this.cache_state[i] == "I"){
					this.Cache_Content[i][1] = "";
					this.Cache_Content[i][2] = "";
					color[i] = Gray;
				}
				else{
					this.Cache_Content[i][1] = this.cache_op[i];
					this.Cache_Content[i][2] =  Integer.toString(this.cache_addr[i]);
					// System.out.println(this.cache_state[i]);
					if(this.cache_state[i] == "M")
						color[i] = Color.PINK;
					else
						color[i] = new Color(0, 197, 205);
				}
				this.table_1.updateUI();
				// this.table_1.setValueAt(this.Cache_Content[i][1], i, 1);
				// this.table_1.setValueAt(this.Cache_Content[i][2], i, 2);
			}
			this.setColor(table_1, color);

		}

		public void actionPerformed(ActionEvent e){
			/******编写自己的处理函数*******/

			this.simulate_cache();

			panel[0].show_cache();
			panel[1].show_cache();
			panel[2].show_cache();
			panel[3].show_cache();
			
			/**********显示刷新后的数据********/
			panel[0].setVisible(false);
			panel[0].setVisible(true);
			panel[1].setVisible(false);
			panel[1].setVisible(true);					
			panel[2].setVisible(false);
			panel[2].setVisible(true);
			panel[3].setVisible(false);
			panel[3].setVisible(true);
		}
	}

    public static void memsetColor(JTable table, int rowIndex, int columnIndex, Color color) {  
        try {  
            DefaultTableCellRenderer tcr = new DefaultTableCellRenderer() {  
  
                public Component getTableCellRendererComponent(JTable table,  
                        Object value, boolean isSelected, boolean hasFocus,  
                        int row, int column) {  
                    if (row == rowIndex) {  
                        setBackground(color);  
                        setForeground(Color.BLACK);  
                    }else if(row > rowIndex){  
                        setBackground(new Color(255,222,173));  
                        setForeground(Color.BLACK);  
                    }else{  
                        setBackground(new Color(255,222,173));  
                        setForeground(Color.BLACK);  
                    }  
  
                    return super.getTableCellRendererComponent(table, value,  
                            isSelected, hasFocus, row, column);  
                }  
            };  

            table.getColumn(table.getColumnName(columnIndex)).setCellRenderer(tcr);  
        } catch (Exception ex) {  
            ex.printStackTrace();  
        }  
    }  	

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		JFrame myjf = new JFrame("多cache一致性模拟之监听法");
		myjf.setSize(1500, 600);
		myjf.setLayout(null);
		myjf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		Container C1 = myjf.getContentPane();
		
		JScrollPane scrollPane2 = new JScrollPane(table_2);
		table_2.getTableHeader().setFont(new Font("华文楷体",0,15));
		table_2.setFont(new Font("华文楷体",0,15));	
		memsetColor(table_2, 0, 0, new Color(255,222,173));
		memsetColor(table_2, 0, 1, new Color(255,222,173));
		memsetColor(table_2, 0, 2, new Color(255,222,173));
		/*****新建panel1*****/
		JPanel panel1 = new JPanel();
		panel[0] = new Mypanel(0);
		panel[1] = new Mypanel(1);
		panel[2] = new Mypanel(2);
		panel[3] = new Mypanel(3);
		C1.add(panel[0]);
		C1.add(panel[1]);
		C1.add(panel[2]);
		C1.add(panel[3]);
		C1.add(info_label);
		C1.add(scrollPane2);
		panel[0].setBounds(10, 100, 350, 200);
		panel[1].setBounds(360, 100, 350, 200);
		panel[2].setBounds(720, 100, 350, 200);
		panel[3].setBounds(1080, 100, 350, 200);
		info_label.setBounds(20,300,380,180);
		scrollPane2.setBounds(400,350,1000,180);
		info_label.setFont(new Font("华文楷体",0,15));
		scrollPane2.setFont(new Font("华文楷体",0,15));
		//scrollPane2.setBounds(100, 250, 310, 180);
		
		/********设置每个Mypanel的不同的参数************/
		panel[0].label_2.setText("Process1");
		panel[1].label_2.setText("Process2");
		panel[2].label_2.setText("Process3");
		panel[3].label_2.setText("Process4");
		panel[0].table_1.getColumnModel().getColumn(0).setHeaderValue("cache1");
		panel[0].Cache_ca[0]="cache1";
		panel[1].table_1.getColumnModel().getColumn(0).setHeaderValue("cache2");
		panel[1].Cache_ca[0]="cache2";
		panel[2].table_1.getColumnModel().getColumn(0).setHeaderValue("cache3");
		panel[2].Cache_ca[0]="cache3";
		panel[3].table_1.getColumnModel().getColumn(0).setHeaderValue("cache4");
		panel[3].Cache_ca[0]="cache4";
		
		
		//panel2.table_2.getColumnModel().getColumn(0).setHeaderValue("Memory1");
		//panel3.table_2.getColumnModel().getColumn(0).setHeaderValue("Memory2");
		//panel4.table_2.getColumnModel().getColumn(0).setHeaderValue("Memory3");
		//panel5.table_2.getColumnModel().getColumn(0).setHeaderValue("Memory4");
		
		for(int i=0;i<10;i++){
			//panel3.Mem_Content[i][0]=String.valueOf((Integer.parseInt(panel3.Mem_Content[i][0])+10));
			//panel4.Mem_Content[i][0]=String.valueOf((Integer.parseInt(panel3.Mem_Content[i][0])+20));
			//panel5.Mem_Content[i][0]=String.valueOf((Integer.parseInt(panel3.Mem_Content[i][0])+30));
		}
		/********设置头部panel*****/
		panel1.setBounds(10, 10, 1500, 100);
		panel1.setLayout(null);
		
		JLabel label1_1=new JLabel("执行方式:单步执行");
		label1_1.setFont(new Font("华文楷体",0,20));
		label1_1.setBounds(15, 15, 200, 40);
		panel1.add(label1_1);
		
		//JComboBox<String> Mylistmodel1_1 = new JComboBox<>(new Mylistmodel());
		Mylistmodel1_1.setBounds(220, 15, 150, 40);
		Mylistmodel1_1.setFont(new Font("华文楷体",0,20));
		panel1.add(Mylistmodel1_1);
		
		JButton button1_1=new JButton("复位");
		button1_1.setFont(new Font("华文楷体",0,18));
		button1_1.setBounds(400, 15, 90, 40);
		
		/**********复位按钮事件（初始化）***********/
		button1_1.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent arg0){
				panel[0].init();
				panel[1].init();
				panel[2].init();
				panel[3].init();
				Mylistmodel1_1.setSelectedItem("直接映射");
				
			}
		});
		
		/*panel2.Mem_Content[1][1]="11";*/
		panel1.add(button1_1);
		C1.add(panel1);
		myjf.setVisible(true);
		

		
	}

	
}

