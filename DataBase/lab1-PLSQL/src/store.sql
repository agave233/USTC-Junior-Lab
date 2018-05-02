create or replace procedure update_BookID(ori_id in char, new_id in char)
as
begin
--  update Borrow
--  set Book_ID = new_id
--  where Book_ID = ori_id;
  execute immediate
  'set constraint FK_BI deferred';
  update Book 
  set id = new_id
  where id = ori_id ;
  
  update Borrow 
  set Book_ID = new_id
  where Book_ID = ori_id ;
  
  execute immediate
  'set constraint FK_BI immediate';
end;