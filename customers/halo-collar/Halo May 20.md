Data Quality Improvement: Outlier rate dropped to 8.1% from 40% across labeled activity classes, improving sample qualification.
Labeler Discrepancies: One labeler caused 50.1% of outlier flags; a double-blind review will target training improvements.
Missing App Logs: App logs are missing for 20-30 files; an audit will recover these logs to ensure full data alignment.
Model Accuracy: The activity model achieved 90% accuracy with a cleaned dataset; deployment will merge activity and GPS models.
GPS Model Testing: The GPS model is complete but needs diverse data for improved generalization; automated training will update it.
Labeling Clarity Needed: More precise definitions for walking, running, and sniffing are important to enhance labeling consistency and model relevance.

Notes
Data Quality and Labeling Accuracy
The team has improved sample qualification significantly, achieving a much lower outlier rate than before.

Outlier rate reduced to about 8.1% across seven labeled activity classes from multiple callers (09:06)

This is a major improvement over previous data with roughly 40% flagged outliers.
Outliers were identified using multiple random forest models voting on outlier status and cluster distance metrics.
Some outliers arise from transitional movements, which the team currently flags to maintain clean labels.
There is potential future work to include transitional states in model training, but for now clean data is preferred.
Certain labelers/callers contribute disproportionately to outliers, with one individual responsible for 50.1% of flags (08:18)

The team plans a double-blind analysis to confirm problematic labelers without bias.
This insight will help target training or feedback to improve labeling consistency.
Michael Ehrman highlighted the need for faster feedback loops to data providers to catch such issues early.
Missing app logs for some files hinder full data alignment, impacting roughly 20-30 files (03:20)

Dinko will audit and ping data providers to recover missing app logs.
This gap mostly involves missing app logs rather than collar data.
The team discussed automating file delivery to reduce errors caused by manual email sending.
Proposed automation includes centralized Google Drive upload with metadata comments and backend file processing (13:19)

This would enable automatic detection, analysis, and feedback to data submitters.
Ivan Turasov mentioned using Edge Impulse data pipelines to automate ingestion, training, and reporting.
Integrations with S3 or Azure Blob Storage are also considered to streamline the process.
Automating feedback will improve turnaround and data quality long-term.
Activity Model Development and Deployment
The activity classification model shows promising accuracy and is ready for integration and further testing with live data.

Activity model currently achieves about 90% accuracy with the new cleaned data set (04:44)

The model uses 2-second windows and seven activity classes.
Data quality improvements have contributed to this enhanced performance.
Dinko has set up a daily pipeline to automate data ingestion and model retraining.
Model deployment will combine activity and GPS models into a single SDK package to avoid inference clashes (23:07)

Ivan Turasov outlined that models are generated with unique IDs but require manual integration into firmware.
The team plans to deploy an updated activity model with reduced classes and test it live on the collar device.
Testing live will validate if the reduced four-class model accurately reflects real dog behaviors.
Current model limitations include overlapping labels like walking and sniffing, which complicate classification (25:04)

Michael Ehrman emphasized the need to clarify sniffing as a static behavior, distinct from walking.
The team agreed to refine label definitions in the app for better annotation consistency.
Running is a critical class for detecting ground movement and needs more data.
Feature reduction is considered but not critical due to already small model size and fast inference (20:57)

Ivan suggested that removing some input features would not significantly reduce latency or memory use.
Michael raised concerns about flash memory usage, indicating some optimization might help.
Dinko noted Edge Impulse's current lack of feature importance tools but could explore light GBM models for this.
GPS Model Status and Data Sufficiency
The GPS classification model is complete but awaiting deployment and additional data integration.

GPS model is trained and performing well on existing data but latest data not yet ingested (17:10)

Dinko confirmed the model is created within Edge Impulse and just needs deployment to the collar.
New GPS data received in the last two weeks will be added soon to improve the model.
The current data set has clear cases such as indoor blocked and outdoor covered GPS signals.
Data sufficiency is limited for some GPS states, requiring more diverse examples (17:39)

The team recognizes the need for more varied conditions to ensure model generalization.
Ivan and Michael stressed validating if the model generalizes well beyond training data.
Automated pipelines are set up to retrain the GPS model as new data arrives (19:28)

This system supports continuous improvement and quick updates.
Future efforts will likely focus on testing and refining the GPS model alongside activity data.
Process Improvements and Automation
The team aims to improve data collection workflows with automation to boost efficiency and data reliability.

Current manual email-based file submissions cause delays and missing data issues (14:04)

Human error risks include forgetting to send attachments.
Centralized upload to a Google Drive folder is proposed to replace email attachments.
Mobile team will be engaged to modify app workflow to support this.
Edge Impulse data pipelines can automate ingestion, analysis, training, and reporting (14:18)

Automated daily or weekly runs would identify new files and generate outlier reports.
This reduces manual work and speeds up feedback to labelers.
Integration with cloud storage solutions like Azure or S3 is possible for seamless data flow.
Feedback loops to data providers will be shortened to improve data quality and adherence (11:07)

Michael emphasized the need for rapid acknowledgment of received files and error reports.
Automated messaging after file processing will inform submitters of data quality and flags.
Faster feedback helps keep experienced data providers engaged and improves overall data sets.
Labeling Guidance and Behavioral Definitions
Clearer labeling instructions and class definitions are needed to improve data quality and model relevance.

Walking, running, and sniffing behaviors need more precise definitions to reduce overlap (25:16)

Sniffing should be labeled only when the dog is stationary and moving its head.
Walking and running indicate movement along the ground and are mutually exclusive with sniffing.
Michael plans to instruct labelers accordingly to improve consistency.
Current model does not include eating or drinking behaviors, which may cause classification gaps (26:07)

These behaviors look similar to standing and need separate handling.
Future data collection and labeling may add these classes.
Labeling guidelines will help ensure the activity model aligns with real-world use cases (27:11)

Michael noted the importance of distinguishing moving vs. not moving for key use cases.
Labelers will be advised that any ground movement is walking or running.
This clarity will improve the model’s practical value for monitoring dog activity.

Action items
Dinko Osmankovic
Investigate missing app logs causing data alignment issues and follow up with data providers to supply the missing files. Create a list or report of these missing logs and request updates either in the group or through direct contacts (11:00)
Add the latest GPS data received to the existing GPS model dataset and retrain the model to incorporate the new data for improved accuracy (19:15)
Michael Ehrman
Coordinate with the mobile app team to implement an automated data upload and feedback system to replace email attachments, potentially using a centralized Google Drive folder or integrated app functionality (13:00)
Explore backend process improvements to automatically move, analyze, and provide feedback on received data files, leveraging Edge Impulse data pipelines for automation (15:20)
Ivan Turasov
Work on integrating and deploying both activity and GPS models into a single SDK package, resolving symbol clashes and ensuring compatibility with multi-project deployment features (22:55)
Implement automation of data quality reports and model retraining using Edge Impulse data pipeline features once the data upload process is improved and stabilized (14:45)
Prepare to disable minimal classes and adjust data sampling to focus on four core activity classes for the next model training iteration to improve classification accuracy (23:30)
All Team
Adjust labeling instructions for behaviors such as sniffing to explicitly define them as stationary head movements to reduce ambiguity in data annotation and improve model interpretability (25:20)
