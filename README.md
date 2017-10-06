# bardiReaderPi

1. buat table di posgree

````
CREATE TABLE "public"."tjobmachinereader" (
  "id" int4 NOT NULL DEFAULT nextval('tjobmachinereader_id_seq'::regclass),
  "nosalesorder" varchar(64) COLLATE "pg_catalog"."default" NOT NULL DEFAULT NULL,
  "machine_id" int4 NOT NULL DEFAULT NULL,
  "jobdate" timestamp(6) DEFAULT NULL,
  "makereadytime" timestamp(6) DEFAULT NULL,
  "makereadyoutput" int4 DEFAULT NULL,
  "productivetime" timestamp(6) DEFAULT NULL,
  "productiveoutput" int4 DEFAULT NULL,
  "finishtime" timestamp(6) DEFAULT NULL,
  "finishoutput" int4 DEFAULT NULL,
  "statusjob" varchar(5) COLLATE "pg_catalog"."default" DEFAULT NULL,
  "jenisjob" varchar(5) COLLATE "pg_catalog"."default" DEFAULT NULL,
  "idgen" uuid DEFAULT gen_random_uuid(),
  CONSTRAINT "pk_tjobmachinereader" PRIMARY KEY ("nosalesorder", "machine_id"),
  CONSTRAINT "tjobmachinereader_id_key" UNIQUE ("id")
)
;

ALTER TABLE "public"."tjobmachinereader" 
  OWNER TO "postgres";
````
2. install pyCharm

