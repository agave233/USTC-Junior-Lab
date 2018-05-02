begin
  insert into Borrow values('BK001', 'RMA098',to_date('2018-01-02', 'yyyy-mm-dd'), to_date('2018-03-02', 'yyyy-mm-dd'));
  insert into Borrow values('BK002', 'RMA098',to_date('2018-02-05', 'yyyy-mm-dd'), null);
  insert into Borrow values('BK006', 'RMA098',to_date('2018-01-22', 'yyyy-mm-dd'), to_date('2018-04-08', 'yyyy-mm-dd'));
  
  insert into Borrow values('BK007', 'RMA099',to_date('2018-02-15', 'yyyy-mm-dd'), null);
  insert into Borrow values('BK008', 'RMA099',to_date('2018-02-16', 'yyyy-mm-dd'), null);
  insert into Borrow values('BK005', 'RMA099',to_date('2018-02-17', 'yyyy-mm-dd'), null);
  insert into Borrow values('BK001', 'RMA099',to_date('2018-03-04', 'yyyy-mm-dd'), to_date('2018-04-02', 'yyyy-mm-dd'));
  
  insert into Borrow values('BK003', 'RMA007',to_date('2017-08-15', 'yyyy-mm-dd'), to_date('2018-01-02', 'yyyy-mm-dd'));
  insert into Borrow values('BK004', 'RMA007',to_date('2017-03-18', 'yyyy-mm-dd'), to_date('2018-01-02', 'yyyy-mm-dd'));
  insert into Borrow values('BK005', 'RMA007',to_date('2017-05-24', 'yyyy-mm-dd'), to_date('2018-01-02', 'yyyy-mm-dd'));
  insert into Borrow values('BK006', 'RMA007',to_date('2017-03-15', 'yyyy-mm-dd'), to_date('2018-01-02', 'yyyy-mm-dd'));
  insert into Borrow values('BK007', 'RMA007',to_date('2017-01-04', 'yyyy-mm-dd'), to_date('2018-01-02', 'yyyy-mm-dd'));
  
  insert into Borrow values('BK001', 'RMA008',to_date('2017-04-19', 'yyyy-mm-dd'), to_date('2017-11-22', 'yyyy-mm-dd'));
  insert into Borrow values('BK002', 'RMA010',to_date('2017-07-28', 'yyyy-mm-dd'), to_date('2018-12-12', 'yyyy-mm-dd'));
  
  insert into Borrow values('BK001', 'RMA011',to_date('2018-04-06', 'yyyy-mm-dd'), null);
  insert into Borrow values('BK002', 'RMA011',to_date('2017-02-04', 'yyyy-mm-dd'), to_date('2017-03-16', 'yyyy-mm-dd'));
  insert into Borrow values('BK004', 'RMA011',to_date('2017-01-15', 'yyyy-mm-dd'), to_date('2017-02-12', 'yyyy-mm-dd'));
  insert into Borrow values('BK005', 'RMA011',to_date('2017-02-14', 'yyyy-mm-dd'), to_date('2018-04-10', 'yyyy-mm-dd'));
  commit;
  dbms_output.put_line('≤Â»Î≥…π¶£°');

end;