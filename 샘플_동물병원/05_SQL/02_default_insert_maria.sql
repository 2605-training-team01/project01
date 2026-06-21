-- MOM
insert into MOM values ('m0001', '010-2251-4546', '강나희', '서울특별시 금천구 가산디지털1로 5');
insert into MOM values ('m0002', '010-4115-4563', '고순희', '서울특별시 금천구 가산디지털2로 10');
insert into MOM values ('m0003', '010-5464-7787', '나사랑', '서울특별시 금천구 가산디지털2로 5');
insert into MOM values ('m0004', '010-2800-2800', '이가은', '서울특별시 관악구 신림로 000');
insert into MOM values ('m0005', '010-8784-5452', '김박사', '서울특별시 금천구 가산디지털2로 331');
insert into MOM values ('m0006', '010-1112-2215', '오윤희', '부산광역시 중구 초량상로 1-4');
insert into MOM values ('m0007', '010-5487-5641', '이보영', '전라북도 전주시 덕진구 전주천동로 455');
insert into MOM values ('m0008', '010-8444-9444', '구억개', '전라북도 전주시 완산구 전주객사3길 67');
insert into MOM values ('m0009', '010-7111-7222', '윤사랑', '서울특별시 성북구 삼양로6길 5');
insert into MOM values ('m0010', '010-8878-5541', '백나윤', '서울특별시 종로구 율곡로27길 7-3');

-- DOGCARD
insert into DOGCARD values ('d0001', '집나간마왕', '말티즈', 3, 3.5, '수컷', sysdate(), 'm0001');
insert into DOGCARD values ('d0002', '아름이', '진돗개', 4, 10.6, '수컷', sysdate(), 'm0002');
insert into DOGCARD values ('d0003', '해피', '말라뮤트', 1, 32.7, '암컷', sysdate(), 'm0003');
insert into DOGCARD values ('d0004', '똥이', '시츄', 13, 5.8, '암컷', sysdate(), 'm0004');
insert into DOGCARD values ('d0005', '개롱이', '불독', 2, 8.9, '암컷', sysdate(), 'm0005');
insert into DOGCARD values ('d0006', '먹보', '치와와', 7, 3.1, '암컷', sysdate(), 'm0006');
insert into DOGCARD values ('d0007', '바다', '닥스훈트', 10, 7.1, '암컷', sysdate(), 'm0007');
insert into DOGCARD values ('d0008', '타래', '골든 리트리버', 2, 6.1, '수컷', sysdate(), 'm0008');
insert into DOGCARD values ('d0009', '구름이', '삽살개', 1, 22.1, '수컷', sysdate(), 'm0009');
insert into DOGCARD values ('d0010', '하얀이', '도베르만', 6, 32.1, '암컷', sysdate(), 'm0010');
insert into DOGCARD values ('d0011', '하얀일', '도베르만', 8, 31.1, '수컷', sysdate(), 'm0010');

-- DISEASE
insert into DISEASE values ('d01', '소화기질환');
insert into DISEASE values ('d02', '심장사상충');
insert into DISEASE values ('d03', '파보바이러스');
insert into DISEASE values ('d04', '기생충');
insert into DISEASE values ('d11', '관절염');
insert into DISEASE values ('d12', '골절 및 절단');
insert into DISEASE values ('d21', '피부병');
insert into DISEASE values ('d22', '귀 염증');
insert into DISEASE values ('d31', '방광염');
insert into DISEASE values ('d41', '백내장');

-- TREAT
insert into TREAT values ('t01', '혈액 검사', 100000, '비급여');
insert into TREAT values ('t02', '내과수술', 700000, '급여');
insert into TREAT values ('t03', '안과수술', 500000, '급여');
insert into TREAT values ('t04', '정형외과수술', 100000, '급여');
insert into TREAT values ('t05', '예방접종', 20000, '비급여');
insert into TREAT values ('t06', '약물 주사', 30000, '급여');
insert into TREAT values ('t07', '연고', 15000, '비급여');
insert into TREAT values ('t08', '물리치료', 35000, '급여');
insert into TREAT values ('t09', '레이저 치료', 150000, '급여');
insert into TREAT values ('t10', '한방 침', 30000, '비급여');

-- HOSPITAL
insert into HOSPITAL values ('h01', '의사부', '김형수');
insert into HOSPITAL values ('h02', '간호부', '맑음소녀');
insert into HOSPITAL values ('h03', '사무부', '수스맨');

-- EMP
insert into EMP values ('e0001', '나똑똑', '010-3564-6545', sysdate(), 35, 5000000, 'h01');
insert into EMP values ('e0002', '신의손', '010-4574-4531', sysdate(), 55, 6000000, 'h01');
insert into EMP values ('e0003', 'JSON', '010-9941-6547', sysdate(), 52, 4500000, 'h01');
insert into EMP values ('e0004', '김사랑', '010-5564-9951', sysdate(), 22, NULL, 'h02');
insert into EMP values ('e0005', '오이쁨', '010-3553-6844', sysdate(), 28, 3500000, 'h02');
insert into EMP values ('e0006', '신예림', '010-8615-6550', sysdate(), 31, 3200000, 'h02');
insert into EMP values ('e0007', '강한나', '010-9518-1526', sysdate(), 33, 4000000, 'h02');
insert into EMP values ('e0008', '김예원', '010-6518-1556', sysdate(), 22, 2500000, 'h03');
insert into EMP values ('e0009', '강수람', '010-6524-7778', sysdate(), 58, 3800000, 'h03');
insert into EMP values ('e0010', '김총무', '010-4553-4551', sysdate(), 40, 2600000, 'h03');
insert into EMP values ('e0011', '김형수', '010-2475-7431', sysdate(), 30, 100, 'h01');
insert into EMP values ('e0012', '맑음소녀', '010-2475-7432', sysdate(), 30, 7000000, 'h02');
insert into EMP values ('e0013', '수스맨', '010-2475-7433', sysdate(), 30, 100, 'h03');

commit;

-- 확인
select * from MOM;
select * from DOGCARD;
select * from DISEASE;
select * from TREAT;
select * from HOSPITAL;
select * from EMP;
