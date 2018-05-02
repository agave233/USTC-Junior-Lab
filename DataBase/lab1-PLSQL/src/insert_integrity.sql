begin
	 insert into Reader values('RMA098', 'Rose1', 20, 'England');
    
	 update Reader 
	 set id = 'RMA096'
	 where id = 'RMA098' ;

	insert into Book values('BK099', '', 'Tom', 22, 0);
end;