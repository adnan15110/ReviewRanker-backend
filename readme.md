## setting up the proxy
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64
chmod +x cloud_sql_proxy
## run the proxy
./cloud_sql_proxy -instances="reviewranker:us-east1:review-ranker-db"=tcp:3306

export GOOGLE_APPLICATION_CREDENTIALS="/Users/Tumul/PycharmProjects/ReviewRankerBackend/ReviewRanker-db.json"
