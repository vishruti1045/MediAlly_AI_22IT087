# MediAlly_AI_22IT087
# Medical Symptom Assistant(LLM):

Healthcare accessibility remains a challenge globally, with patients often struggling to understand their symptoms before seeking medical advice. Delays in diagnosis can lead to worsening conditions, increased healthcare costs, and strain on medical infrastructure. A Medical Symptom Assistant (MSA) aims to bridge this gap by leveraging artificial intelligence (AI) and machine learning (ML) to provide preliminary symptom assessments and suggest possible conditions based on user inputs.

The landscape of AI-driven Medical Symptom Assistants (MSAs) includes various commercial and academic approaches. However, many existing solutions either suffer from low accuracy, lack personalized recommendations, or fail to provide interpretability. Our proposed solution aims to bridge these gaps using a robust machine learning approach that improves accuracy, transparency, and reliability.

<img src="frontend\assets\home1.png" width="650"/>

How Does the Medical Symptom Assistant Work?
Our AI-driven system follows a structured approach to analyze user input and provide meaningful insights:

🔹 Step 1: Input Symptoms

Users enter their symptoms in plain language (e.g., “I have a fever and body aches, and my throat feels sore.”).

🔹 Step 2: Text Processing with NLP

The input is tokenized and processed using BioBERT — a transformer-based deep learning model trained on biomedical text.

🔹 Step 3: Disease Prediction with Deep Learning

The processed text is fed into a custom-trained classification model, which predicts the most likely conditions.

🔹 Step 4: Confidence Score & Risk Categorization

The AI assigns a confidence score to each predicted condition and categorizes the risk level into:

🟢 Green (Home Care) — Mild symptoms that can be managed at home.

🟡 Yellow (Doctor Visit) — Conditions that require medical consultation.

🔴 Red (Emergency) — Urgent conditions that need immediate attention.

<img src="frontend\assets\pred2.png" width="650"/>

<img src="frontend\assets\pred3.png" width="650"/>

🔹 Step 5: ICD-10 Code Mapping

Each predicted disease is mapped to its corresponding ICD-10 code, making it easy for users to understand and communicate with healthcare professionals.

<img src="frontend\assets\accuracy.png" width="650"/>

✅ Overall Accuracy: ~85% on test data.

✅ Precision & Recall: Optimized for high recall to avoid missing serious conditions.

✅ False Negatives: Minimized to prevent misclassification of severe conditions.
