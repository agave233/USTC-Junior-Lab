begin
  insert into Reader values('RMA001', 'Navas', 32, '哥斯达黎加');
  insert into Reader values('RMA020', 'Asensio', 22, '西班牙');
  insert into Reader values('RMA004', 'Ramos', 32, '西班牙');
  insert into Reader values('RMA007', 'Ronaldo', 33, '葡萄牙');
  insert into Reader values('RMA009', 'Benzema', 31, '法国');
  insert into Reader values('RMA011', 'Bale', 32, '威尔士');
  insert into Reader values('RMA008', 'Kroos', 28, '德国');
  insert into Reader values('RMA010', 'Modric', 33, '克罗地亚');
  insert into Reader values('RMA098', 'Rose', 24, '英国');
  insert into Reader values('RMA099', '李林', 21, '中国');
  commit;
  dbms_output.put_line('插入成功！');
exception
  when Dup_val_on_index Then
    dbms_output.put_line('插入失败,主键已存在');
  when others Then
    dbms_output.put_line('插入失败,未知原因');
end;