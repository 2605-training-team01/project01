--MEDICAL
insert into MEDICAL values (date_format(now(), '%y%m%d%H%i%s'), '진단', 'D0001', 'D01', null);
do sleep(1);
insert into MEDICAL values (date_format(now(), '%y%m%d%H%i%s'), '치료', 'D0002', 'D02', 'T02');
do sleep(1);
insert into MEDICAL values (date_format(now(), '%y%m%d%H%i%s'), '치료', 'D0003', 'D03', 'T02');
do sleep(1);
insert into MEDICAL values (date_format(now(), '%y%m%d%H%i%s'), '진단', 'D0004', 'D04', null);
do sleep(1);
insert into MEDICAL values (date_format(now(), '%y%m%d%H%i%s'), '치료', 'D0005', 'D11', 'T04');
do sleep(1);
insert into MEDICAL values (date_format(now(), '%y%m%d%H%i%s'), '치료', 'D0006', 'D12', 'T08');
do sleep(1);
insert into MEDICAL values (date_format(now(), '%y%m%d%H%i%s'), '치료', 'D0007', 'D21', 'T07');
do sleep(1);
insert into MEDICAL values (date_format(now(), '%y%m%d%H%i%s'), '치료', 'D0008', 'D22', 'T07');
do sleep(1);
insert into MEDICAL values (date_format(now(), '%y%m%d%H%i%s'), '진단', 'D0009', 'D31', null);
do sleep(1);
insert into MEDICAL values (date_format(now(), '%y%m%d%H%i%s'), '치료', 'D0010', 'D41', 'T03');


select * from MEDICAL;	--'MEDICAL' 테이블의 데이터 확인
select * from BILL;	--trigger로 생성된 'BILL' 테이블의 데이터 확인