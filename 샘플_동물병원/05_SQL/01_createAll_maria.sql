--mysql -u project -p
--Enter password: java

--show databases;
--use modeling_schema
--show tables;


drop table if exists EMP;
drop table if exists HOSPITAL;
drop table if exists BILL;
drop table if exists MEDICAL;
drop table if exists TREAT;
drop table if exists DISEASE;
drop table if exists DOGCARD;
drop table if exists MOM;

create table MOM (
    M_NUMBER char(5) not null,                 
    M_PHONE varchar(13) not null unique,      
    M_NAME varchar(20) not null,               
    M_ADDR varchar(100) not null,              
    primary key (M_NUMBER)
) engine=innodb default charset=utf8mb4;

create table DOGCARD (
    D_NUMBER char(5) not null,                  
    D_NAME varchar(20) not null,                 
    D_KINDS varchar(50) default null,            
    D_AGE tinyint unsigned default null,         
    D_WEIGHT decimal(4,1) default null,           
    D_SEX enum('수컷', '암컷') default null,         
    D_FDATE datetime default current_timestamp,   
    M_NUMBER char(5) not null,                   
    primary key (D_NUMBER),
    constraint FK_DOGCARD_MOM foreign key (M_NUMBER)
        references MOM (M_NUMBER)
        on delete cascade
) engine=innodb default charset=utf8mb4;

create table DISEASE (
    DS_CODE char(3) not null,                     
    DS_NAME varchar(50) not null,                  
    primary key (DS_CODE)
) engine=innodb default charset=utf8mb4;

create table TREAT (
    T_CODE char(3) not null,                      
    T_HOW varchar(50) not null,                    
    T_COST int not null,                           
    T_INS enum('급여', '비급여') default null,        
    primary key (T_CODE)
) engine=innodb default charset=utf8mb4;

create table MEDICAL (
    MD_DATE varchar(14) not null,                  
    MD_SEC enum('진단', '치료') not null,          
    D_NUMBER char(5) not null,                      
    DS_CODE char(3) default null,                   
    T_CODE char(3) default null,                    
    primary key (MD_DATE),
    constraint FK_MEDICAL_DOGCARD foreign key (D_NUMBER)
        references DOGCARD (D_NUMBER)
        on delete cascade,
    constraint FK_MEDICAL_DISEASE foreign key (DS_CODE)
        references DISEASE (DS_CODE),
    constraint FK_MEDICAL_TREAT foreign key (T_CODE)
        references TREAT (T_CODE)
) engine=innodb default charset=utf8mb4;

create table BILL (
    MD_DATE varchar(14) not null,                   
    B_VCOST int default 15000,                      
    B_TCOST int default null,                        
    primary key (MD_DATE),
    constraint FK_BILL_MEDICAL foreign key (MD_DATE)
        references MEDICAL (MD_DATE)
        on delete cascade
) engine=innodb default charset=utf8mb4;

create table HOSPITAL (
    H_CODE char(3) not null,                         
    H_JOB varchar(50) not null,                       
    H_MGR varchar(20) default null,                   
    primary key (H_CODE)
) engine=innodb default charset=utf8mb4;

create table EMP (
    E_NUMBER char(5) not null,                       
    E_NAME varchar(20) not null,                      
    E_PHONE varchar(13) not null unique,              
    E_HIREDATE datetime default current_timestamp,  
    E_AGE tinyint unsigned default null,              
    E_SAL int default null,                            
    H_CODE char(3) not null,                           
    primary key (E_NUMBER),
    constraint FK_EMP_HOSPITAL foreign key (H_CODE)
        references HOSPITAL (H_CODE)
        on delete cascade
) engine=innodb default charset=utf8mb4;
