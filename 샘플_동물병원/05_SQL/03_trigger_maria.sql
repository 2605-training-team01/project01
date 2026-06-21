-- 트리거 삭제 및 생성 
drop trigger if exists BILL_INSERT;

delimiter $$

create trigger BILL_INSERT
after insert on MEDICAL
for each row
begin
    insert into BILL (MD_DATE, B_VCOST)
    values (new.MD_DATE, default);
end $$

delimiter ;

-- 트리거 확인
show triggers like 'MEDICAL'\G

-- 트리거 사용(insert 예시)
insert into MEDICAL (MD_DATE, MD_SEC, D_NUMBER, DS_CODE, T_CODE)
values (date_format(now(), '%y%m%d%H%i%s'), '치료', 'd0002', 'd22', 't06');

select * from MEDICAL;
select * from BILL;
