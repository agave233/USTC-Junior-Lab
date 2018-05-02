declare
    type rd is record(
      id Reader.ID%type,
      addr Reader.address%type
      );
    s1 rd; 
    
    cursor s2 is select Book.name, Borrow.brrrow_date 
                  from Book, Borrow 
                  where Book.ID = Borrow.book_ID and Borrow.Reader_ID = s1.id;
                  
    cursor s3 is select name 
                  from Reader
                  where id not in (select distinct Reader_ID from Borrow);
    
    cursor s4 is select name, price
                  from Book
                  where author = 'Ullman';
                  
    cursor s5 is select book.id, book.name
                  from Book, Reader, Borrow
                  where Reader.name = '李林' and Reader.id = Borrow.Reader_ID 
                  and Borrow.Book_ID = Book.id and Borrow.return_date is null;
                  
    cursor s6 is select name
                  from Reader, (select Reader_ID, count(Book_ID) as count_book
                                from Borrow
                                group by Reader_ID) Borrow2
                  where Reader.id = Borrow2.Reader_ID and Borrow2.count_book > 3;
    
    cursor s7 is (select name, id from Reader)
                   minus
                  (select distinct Reader.name as name, Reader.id as id
                   from (select distinct Borrow.Book_ID as id
                         from Borrow, Reader
                         where Borrow.Reader_ID = Reader.id and Reader.name = '李林') BookID,
                         Borrow,Reader
                   where Borrow.Book_ID in BookID.id and Borrow.Reader_ID = Reader.id);
      
    cursor s8 is select id, name 
                  from Book
                  where name like '%Oracle%';
    
    view_exist number;
    type br is record(
      Reader_id Reader.id%type,
      Reader_name Reader.name%type,
      Book_id Book.id%type,
      Book_name Book.name%type,
      Borrow_date Borrow.Brrrow_date%type
      );
    s9 br; 
begin
-- (1)
    select ID, address into s1 from Reader where name = 'Rose';
    DBMS_OUTPUT.PUT_LINE('（1）检索读者Rose 的读者号和地址: ' || s1.id || s1.addr);
-- (2)
    DBMS_OUTPUT.PUT_LINE('（2）Rose所借的图书的图书名和借期：');
    DBMS_OUTPUT.PUT_LINE('-------------------------');
    for s in s2 loop
      DBMS_OUTPUT.PUT_LINE(rpad(s.name, 8) || s.brrrow_date);
    end loop;
    DBMS_OUTPUT.PUT_LINE('-------------------------');
-- (3)
    DBMS_OUTPUT.PUT_LINE('（3）未借阅图书的读者姓名：');
    DBMS_OUTPUT.PUT_LINE('-------------------------');
    for s in s3 loop
      DBMS_OUTPUT.PUT_LINE(s.name);
    end loop;
    DBMS_OUTPUT.PUT_LINE('-------------------------');
-- (4)
    DBMS_OUTPUT.PUT_LINE('（4）Ullman所写的书的书名和单价：');
    DBMS_OUTPUT.PUT_LINE('-------------------------');
    for s in s4 loop
      DBMS_OUTPUT.PUT_LINE(rpad(s.name, 10) || rpad(s.price, 2));
    end loop;
    DBMS_OUTPUT.PUT_LINE('-------------------------');
-- (5)
    DBMS_OUTPUT.PUT_LINE('（5）李林借阅未还的图书的图书号和书名：');
    DBMS_OUTPUT.PUT_LINE('-------------------------');
    for s in s5 loop
      DBMS_OUTPUT.PUT_LINE(rpad(s.id, 10) || rpad(s.name, 20));
    end loop;
    DBMS_OUTPUT.PUT_LINE('-------------------------'); 
-- (6)
    DBMS_OUTPUT.PUT_LINE('（6）借阅图书数目超过 3 本的读者姓名：');
    DBMS_OUTPUT.PUT_LINE('-------------------------');
    for s in s6 loop
      DBMS_OUTPUT.PUT_LINE(s.name);
    end loop;
    DBMS_OUTPUT.PUT_LINE('-------------------------'); 
-- (7)
    DBMS_OUTPUT.PUT_LINE('（7）没有借阅读者"李林"所借的任何一本书的读者姓名和读者号：');
    DBMS_OUTPUT.PUT_LINE('-------------------------');
    for s in s7 loop
      DBMS_OUTPUT.PUT_LINE(rpad(s.id, 10) || rpad(s.name, 20));
    end loop;
    DBMS_OUTPUT.PUT_LINE('-------------------------');    
-- (8)
    DBMS_OUTPUT.PUT_LINE('（8）书名中包含“Oracle”的图书书名及图书号：');
    DBMS_OUTPUT.PUT_LINE('-------------------------');
    for s in s8 loop
      DBMS_OUTPUT.PUT_LINE(rpad(s.id, 10) || rpad(s.name, 20));
    end loop;
    DBMS_OUTPUT.PUT_LINE('-------------------------');   
-- (9)
    select count(1) into view_exist from user_views where view_name=upper('borrow_info');
    if view_exist = 0 then 
      execute immediate 
      'create view borrow_info(Reader_id, Reader_name, Book_id, Book_name, Borrow_date)
      as select Reader.id, Reader.name, Book.id, Book.name, Borrow.Brrrow_date
          from Reader, Book, Borrow
          where Reader.id = Borrow.Reader_ID and Book.id = Borrow.Book_ID
      with read only';
      DBMS_OUTPUT.PUT_LINE('视图创建成功！');  
    end if;
    
    DBMS_OUTPUT.PUT_LINE('（9）最近一年所有读者的读者号以及所借阅的不同图书数：');
    DBMS_OUTPUT.PUT_LINE('-------------------------');   
    for c1 in(select Reader_id, count(distinct Book_id) as br_num
              from borrow_info 
              where sysdate - Borrow_date < 365 group by Reader_id) loop
      DBMS_OUTPUT.PUT_LINE(rpad(c1.Reader_id, 10) || c1.br_num);
    end loop;
    DBMS_OUTPUT.PUT_LINE('-------------------------');   
--DBMS_OUTPUT.PUT_LINE(sysdate-to_date('2018-03-20','yyyy--mm-dd'));

--  exception
--    when NO_DATA_FOUND then
--        DBMS_OUTPUT.PUT_LINE('找不到数据');
--    when others then
--        DBMS_OUTPUT.PUT_LINE('未知错误');
end;