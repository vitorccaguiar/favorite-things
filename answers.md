# Answers

### How long did you spend on the coding test below?

Since I never worked before with any of these technologies/frameworks I took some time to study them and do some samples. Therefore I spent 48 hours (6 days).

### What would you add to your solution if you had more time?

I would:
- Finish the Audit Log logic
- Create the tests
- Create a service layer for the frontend in order to separate the API calls from the Vue components
- Create frontend and backend validations

### What was the most useful feature that was added to the latest version of your choosen language?

Was not really needed to use a specific feature from JavaScript or Python but I can name some interesting features from the new ECMAScript (2019). Such as **Object.fromEntries** that you can transform iterables into objects and **String.trimEnd** that you can remove white spaces at the end of a string.

### How would you track down performance issue in production? Have you ever had to do this?

I would use some solution like Kibana + Elasticsearch + Logstash. I helped once to configure those for a legacy system that was having performance issues. After that we identified some methods that were not well implemented and the client was calling it a lot, then we put effort to refactor them. Also was possible to see when the system was about to shutdown and take actions beforehand to avoid that. The Logstash colleted the logs from the system and converted to something meaningful, the output was added into the elasticsearch and the Kibana was configured to use the elasticsearch.