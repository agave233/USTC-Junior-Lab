create table Book(
  ID char(8) Constraint PK_B Primary Key,
  name varchar2(10) Not null,
  author varchar2(10),
  price float,
  status int default 0
  );
create table Reader(
  ID char(8) Constraint PK Primary Key,
  name varchar2(10),
  age int,
  address varchar2(20)
  ); 
  create table Borrow(
  book_ID char(8),
  Reader_ID char(8),
  Brrrow_Date date,
  Return_Date date,
  Constraint PK_BR Primary Key(book_ID, Reader_ID),
  Constraint FK_BI Foreign Key(book_ID) References Book(ID),
  Constraint FK_RI Foreign Key(Reader_ID) References Reader(ID)
  );
