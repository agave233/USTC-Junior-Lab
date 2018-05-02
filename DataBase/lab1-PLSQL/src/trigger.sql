create or replace trigger SetStatus
after insert or update of return_date on Borrow
--declare
--  new_status int;
--  book_id book.id%type;
begin
--    select count(*) into new_status 
--    from Book
--    where id in (select Book_ID from Borrow where return_date is null) and status = 0;
    
-- insert(borrow)
    update Book
    set status = 1
    where id in (select Book_ID from Borrow where return_date is null) and status = 0;
-- update(return)
    update Book 
    set status = 0
    where id in ((select distinct Book_ID from Borrow) 
                  minus 
                  (select Book_ID from Borrow where return_date is null)) 
                  and status = 1;
  
  
end;

-- test
-- insert into Borrow values('BK004', 'RMA008',to_date('2018-04-08', 'yyyy-mm-dd'), null);
-- update borrow set return_date = to_date('2018-04-09','yyyy-mm-dd') where reader_id = 'RMA008' and book_id = 'BK004';
-- delete from borrow where reader_id = 'RMA008' and book_id = 'BK004';