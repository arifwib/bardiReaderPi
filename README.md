# bardiReaderPi

1. buat table di posgree
create table tjobmachinereader(
        id serial unique,
        nosalesorder varchar(64) not null,
        machine_id int4,
        jobdate timestamp(6),
        makereadytime timestamp(6),
        makereadyoutput int4,
        productivetime timestamp(6),
        productiveoutput int4,
        finishtime timestamp(6),
        finishoutput int4,
        statusjob varchar(5),
        jenisjob varchar(5),
        CONSTRAINT PK_tjobmachinereader primary key(nosalesorder,machine_id)
        );
