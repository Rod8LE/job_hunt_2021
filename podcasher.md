# Excercise
In this exercise, we have a small, data scenario. We will explain both what the data consists of and the objectives of what we want to do with the data. While this is like a data problem we actually have, we have greatly simplified it so try to keep the scope and unknowns low. 

What we are looking for is how you would approach the problem and what solutions you may consider. We do not need specific software or tools, unless you have a specific one you feel would be well-suited for the task. 
### Scenario 
We have multiple sources of data that provide the number of times a podcast (and its episodes) has been listened to in a month. We need to be able to create a pipeline to inject this data and store it in a way that allows us to both utilize the data in our algorithms but also provide some of the numbers to our pro users. In this problem, assume we have 5 different podcast hosting providers, each represent 10% of the market. (i.e. our data would only represent 50% of all listens). With the data provided by these hosting providers, some provide the number of times each episode of each podcast has been listened to and other hosting providers only the number of times a podcast has been listened to. Additionally, the providers can provide this data:
- Instantly, when the listen occurs
- As a data file daily (either CSV or JSON)
- As a data file monthly (either CSV or JSON)

### Objectives

We would like to use this data to:
- Create estimates for how many times a podcast is listened to in a month and be able to send those estimates to the frontend of the website
- Identify trends, including podcasts that are getting more popular
- Determine how popular certain creators are (by analyzing each episode they appear on other creators)
- Determine how many times an episode is listened to within the first 30 days

### Questions 
After reading over the scenario and objectives, answer the following questions. We understand that there are probably still many unknowns and questions you would need to answer before providing a “real” solution. So, feel free to state when you would need more information and what you would look for.
- How would you approach this scenario?
- How would you design a pipeline (or series of pipelines)to ingest the data?
- How would you approach designing how we store thedata?
- What questions would you need to be answered?


# Response to excercise
Hello! In this document I will tackle and explain the brainstorming that happens when I focus on the proposed scenario. Let this document be a brief explanation of a few topics and ideas I can propose in order to enhance any idea, or issue proposed.
### Scenario assumed:
- We got multiple sources of data that provide the number of times a podcast (and its episodes) has been listened to in a month.
- We need to be able to create a pipeline to inject this data and store it in a way that allows us to both utilize the data in our algorithms but also provide some of the numbers to our pro users.
  -  We need clean and ingestible data for any purpose (reports, algorithms, …)
  - We need great levels of granularity and flexibility (we do not know a priori who, how, what, or why, needs this data nor in which format)
- We have 5 different podcast hosting providers, each representing 10% of the market. (i.e. our data would only represent 50% of all listens).
  - One provider has the number of times each episode of each podcast has been listened to
  - Other hosting providers only provide the number of times a podcast has been listened to.
- We got different ingest frequencies:
  - Instantly, when the listen occurs (so we need to be always up and listening)
  - As a data file daily (either CSV or JSON)
  - As a data file monthly (either CSV or JSON)

### Objectives
We would like to use this data to:
- Create estimates for how many times a podcast is listened to in a month and be able to send those estimates to the frontend of the website
- Identify trends, including podcasts that are getting more popular
- Determine how popular certain creators are (by analyzing each episode they appear onvs other creators)
- Determine how many times an episode is listened to within the first 30 days

Note: all these requirements express the dire need to bring data from one side to another, specifically speaking, in the sense of data availability for either the front end, or as a report for our business units, or the final consumer (as in data consumer, or report watcher)
### Questions
There ARE still many unknowns and questions we need to answer before providing a “real” solution. So, I will try to state when more information is required and what would I look for
- How would you approach this scenario?
  - Short answer: with my best :), many different approaches can be taken
  - I believe consensus is a must in most decisions
- How would you design a pipeline (or series of pipelines)to ingest the data?
  - Short answer: with scalability, data availability, and flexibility in mind.
- How would you approach designing how we store the data?
  - Short answer: in phases and blocks with different access privileges
- What questions would you need to be answered?
  - First I would ask what is expected from the data, what we have, and which resources we got, as detailed as possible

### Solution brainstorm
This is no trivial task, so let me be very clear, we do need enhancements and I am assuming we have nothing in place

First things first we need  COMPLETE CONTROL of our inputs, regardless of the moment, we need to be sure that all our inputs are secured, and in our control. In order to centralize our information we do need to keep every single source stable and prioritize ingestion.
#### Ingestion
That being said, I would store every single bit of data in its raw form somewhere, either a AWS bucket, or a cheap cold-state disk as a copy.
- Cold state copies would let us repair our database in case of doom happens
- I am assuming al data need to be cleaned first and then centralized
- Every input from every provider would stay in our control for X days, depending on budget
- Instant inputs are easy, those can be ingested directly to the database via queries or calls
  - Such instant inputs can be used to feed live metrics, final data consumers can see live data as long as such data can be ingested from instant sources
- Daily/monthly text files, need to be cleaned, processed and formatted (I would do that using python) as quick as such files become available
  - Having and orchestrator (Airflow) in order to constantly check whenever such files are ready or not would help us keep track on hundred or thousands of processes without wasting time on manually ingesting each of them

#### Processing
Data architecture is like plumbing, we need a complete map of where things are coming from, who needs them, why is such data so important, where is needed to stay clean and ready, and how things are expected.

Most of the time, some of these questions can only be answered when things break and/or something is not working well. Let us build a system that tries to be flexible enough for anyone to be able to request, enhance, or add something quickly if needed.

- If we have small inputs, we should have a distributed system, so we can scale, lambdas are great for these kind of topics
- If we got big inputs we need to structure that input so we can SQL our way into a clean table, nothing like AWS deciding how many thousands of processors are required for such task instead of us doing the heavy lifting with monolithic instances
- All inputs need to be cleaned, processed, and LOGGED, that way we can connect an orchestrator like airflow and see how it works and breaks, without having a single developer MANUALLY adding the input every single day
- Things break all the time, it is easier to repair an automated pipeline than manually re-update the whole system every thursday
- If several sources have the same information and different results, we can set a priority system where depending on user feedback, consistency, or any other metric, one provider would have a bigger pull when merging different sources of data
- We can set a phase where our internal customers (marketing or finance team) can decide which SQL needs to run in order for their reports to work
  - Such SQL or python script or whatever, can be automated and added in each deploy for it to be executed every [insert customer-selected date here]
- Data expectation need to be set in order for the cleaning to happen correctly, this is a must


#### Availability
Data needs a specific format to work, from casting a number into a string because a model requires it, to merging all the user data into a single average for a report of the “ model-customer” required by the marketing team. Data needs to look accordingly to each eye or it will not be able to communicate all its value.
- Live models require live data, so such info must be present or available at the same instance, or architecture where the model is being executed.
- Reports can handle a variety of different ports since such things can be generated by our python infrastructure or connected via the many ports of Tableau
- Most of the time, if we have a map of all the data we need and in which frequency it is required we can build “views” or “wrappers” with such frequency that hold a representation of the data required
- Depending on the data consumer needs, different accesses can be set to enhance security, logging, and control
  - Raw data copies can only be accessed by developers or miners
  - Structured data can be accessed by data scientists, models, reports
  - Super cleaned data tables can be accessed by business units, reports, Front end, back end, …

### Example
With all the unknowns, I will try to be brief in what I would expect for a system with the mentioned requirements to have to consider in order to work

- All inputs have a first phase where the feed is checked to see if the input is ready or not to be ingested regardless of frequency, this can be easily adjust to each provider
- Next phase would be to have all data stored in raw form
- Next phase would be to clean such data and process it
  - I would suggest to use either AWS lambdas or direct SQL queries in order to do the heavy lifting instead of having a monolithic instance compute every single repair
- Next phase would be to add such clean data in its own respective table/home
  - Propagate the end of this process to all consumers of this data
- With all data cleaned a “view” or wrapper table, would be available in order to centralize such info
  - I believe we would spam “coalesce” a lot here depending on the case
- Different data from different providers suggest different levels of veracity
  - More complex algorithms would summarize our data into something more user friendly at the cost of losing granularity
- Data consumers within the company should have the ability to choose the level of granularity (I call this data flexibility)
- An auditing system to check our known expectations to avoid “surprises”
  - Before creating a view or reports, check if such data is available or updated

## Wrap up

That being said, for any question please ping me so, looking forward to our next call
