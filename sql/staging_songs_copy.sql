COPY stg_songs FROM {}
credentials 'aws_iam_role={}'
json 'auto' compupdate off region 'us-west-2';
