import sqlite3, json, hashlib, secrets, os

DB_PATH = "data/app.db"

def hp(password):
    salt = secrets.token_hex(16)
    return f"{salt}${hashlib.sha256((salt + password).encode()).hexdigest()}"

def seed():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password_hash TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE notes (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, raw_text TEXT, summary TEXT, concepts TEXT DEFAULT '[]', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE quiz_results (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, note_id INTEGER, score INTEGER, total_questions INTEGER, answers TEXT DEFAULT '[]', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    """)

    for u in ["pavan", "pravinesh", "ashwin", "sneha", "rahul", "divya"]:
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?,?)", (u, hp("test1234")))

    notes = [
        (1, "BPSK maps binary data to two phases separated by 180 degrees. BER = Q(sqrt(2Eb/N0)) in AWGN. QPSK uses four phases transmitting 2 bits per symbol doubling spectral efficiency. Coherent detection requires carrier synchronization. The matched filter maximizes SNR at the decision instant. Differential BPSK avoids carrier sync but has 1dB worse BER.",
         "BPSK uses two phases for binary modulation with BER = Q(sqrt(2Eb/N0)). QPSK doubles spectral efficiency with four phases. Coherent detection needs carrier sync and matched filters maximize SNR. DBPSK avoids sync at cost of 1dB performance.",
         [{"name": "phase shift keying", "score": 0.85}, {"name": "bit error rate", "score": 0.82}, {"name": "QPSK modulation", "score": 0.78}, {"name": "coherent detection", "score": 0.71}, {"name": "matched filter", "score": 0.68}]),

        (1, "Machine learning includes supervised unsupervised and reinforcement learning. Supervised uses labeled data with algorithms like linear regression decision trees random forests and SVMs. Neural networks learn non-linear patterns. Gradient descent minimizes loss functions. L1 and L2 regularization prevents overfitting. Cross validation evaluates model performance.",
         "ML has three types. Supervised learning uses labeled data with regression trees forests and SVMs. Neural networks handle non-linear patterns. Gradient descent optimizes and regularization prevents overfitting.",
         [{"name": "supervised learning", "score": 0.88}, {"name": "gradient descent", "score": 0.82}, {"name": "neural networks", "score": 0.79}, {"name": "regularization", "score": 0.74}, {"name": "overfitting", "score": 0.65}]),

        (2, "Operating systems manage hardware and provide services. Process scheduling uses FCFS SJF and Round Robin algorithms. Virtual memory extends physical memory through paging. Page replacement algorithms include FIFO LRU and Optimal. Deadlock occurs from circular wait and is prevented by resource ordering or bankers algorithm.",
         "OS handles scheduling with FCFS SJF and Round Robin. Virtual memory uses paging. Page replacement with FIFO LRU Optimal. Deadlock prevented by resource ordering.",
         [{"name": "process scheduling", "score": 0.86}, {"name": "virtual memory", "score": 0.81}, {"name": "page replacement", "score": 0.77}, {"name": "deadlock prevention", "score": 0.73}]),

        (2, "CNNs process images through convolutional layers that detect features and pooling layers that reduce dimensions. Key architectures include LeNet AlexNet VGGNet and ResNet with skip connections. Transfer learning adapts pretrained models for new tasks. Data augmentation with rotation flipping and cropping increases training diversity.",
         "CNNs use convolution for features and pooling for dimension reduction. ResNet introduced skip connections. Transfer learning and data augmentation improve results with limited data.",
         [{"name": "convolutional neural networks", "score": 0.89}, {"name": "transfer learning", "score": 0.83}, {"name": "skip connections", "score": 0.74}, {"name": "neural networks", "score": 0.70}]),

        (3, "Database normalization reduces redundancy. 1NF requires atomic values. 2NF removes partial dependencies. 3NF eliminates transitive dependencies. SQL JOINs combine tables with INNER LEFT and CROSS joins. B-tree indexes speed up queries. ACID properties ensure reliable transactions with atomicity consistency isolation durability.",
         "Normalization with 1NF 2NF 3NF reduces redundancy. SQL JOINs combine tables. B-tree indexes speed queries. ACID ensures transaction reliability.",
         [{"name": "database normalization", "score": 0.87}, {"name": "SQL joins", "score": 0.82}, {"name": "ACID properties", "score": 0.78}, {"name": "indexing", "score": 0.73}]),

        (4, "Fourier Transform converts time domain signals to frequency domain. FFT computes DFT efficiently with O(N log N) complexity. FIR filters have linear phase while IIR filters are more efficient. Z-transform analyzes discrete time systems. Nyquist theorem requires sampling at twice the maximum frequency to avoid aliasing.",
         "Fourier Transform and FFT enable frequency analysis. FIR and IIR filters process signals differently. Z-transform analyzes digital systems. Nyquist requires 2x sampling rate.",
         [{"name": "Fourier transform", "score": 0.88}, {"name": "FFT algorithm", "score": 0.83}, {"name": "digital filters", "score": 0.78}, {"name": "Nyquist rate", "score": 0.71}]),

        (4, "ML model evaluation uses precision recall F1-score and ROC-AUC beyond simple accuracy. K-fold cross validation provides robust performance estimates. Bias-variance tradeoff explains underfitting vs overfitting. Ensemble methods like bagging and boosting combine models for better generalization.",
         "Evaluation uses precision recall F1 and ROC-AUC. Cross validation with k-fold gives robust estimates. Bias-variance tradeoff balances complexity. Ensembles improve generalization.",
         [{"name": "model evaluation", "score": 0.86}, {"name": "cross validation", "score": 0.78}, {"name": "bias variance tradeoff", "score": 0.75}, {"name": "overfitting", "score": 0.63}]),

        (5, "Computer networks follow the OSI 7 layer model. TCP provides reliable delivery through three-way handshake flow control and congestion control with algorithms like TCP Reno and Cubic. UDP is connectionless and faster but unreliable. DNS resolves domain names. HTTPS uses TLS encryption for secure web communication.",
         "OSI has 7 layers. TCP ensures reliable delivery via handshake and congestion control. UDP is faster but unreliable. DNS resolves domains and HTTPS uses TLS.",
         [{"name": "OSI model", "score": 0.85}, {"name": "TCP handshake", "score": 0.81}, {"name": "congestion control", "score": 0.77}, {"name": "DNS resolution", "score": 0.69}]),

        (6, "NLP enables computers to understand language. Tokenization splits text into words. Word2Vec and GloVe create word embeddings. Transformers use self-attention to weigh token relationships. BERT provides bidirectional understanding while GPT generates text autoregressively. Applications include named entity recognition and sentiment analysis.",
         "NLP uses tokenization and embeddings. Transformers with self-attention revolutionized the field. BERT understands bidirectionally and GPT generates autoregressively.",
         [{"name": "transformer architecture", "score": 0.89}, {"name": "self attention", "score": 0.84}, {"name": "word embeddings", "score": 0.80}, {"name": "neural networks", "score": 0.72}]),

        (6, "Gradient descent has three variants batch stochastic and mini-batch. Learning rate scheduling improves convergence. Batch normalization stabilizes training. Dropout randomly deactivates neurons to prevent overfitting. Backpropagation computes gradients via chain rule. Common loss functions include MSE for regression and cross-entropy for classification.",
         "Gradient descent variants optimize models. Batch norm and dropout improve training. Backpropagation computes gradients. MSE and cross-entropy are key loss functions.",
         [{"name": "gradient descent", "score": 0.87}, {"name": "backpropagation", "score": 0.83}, {"name": "batch normalization", "score": 0.79}, {"name": "overfitting", "score": 0.62}]),
    ]

    for uid, raw, summ, concepts in notes:
        conn.execute("INSERT INTO notes (user_id, raw_text, summary, concepts) VALUES (?,?,?,?)",
                     (uid, raw, summ, json.dumps(concepts)))

    quizzes = [(1,1,4,5),(1,2,3,5),(2,3,5,5),(2,4,4,5),(3,5,3,5),(4,6,4,5),(4,7,5,5),(5,8,3,5),(6,9,4,5),(6,10,4,5)]
    for uid, nid, score, total in quizzes:
        conn.execute("INSERT INTO quiz_results (user_id, note_id, score, total_questions, answers) VALUES (?,?,?,?,?)",
                     (uid, nid, score, total, "[]"))

    conn.commit()
    conn.close()
    print("Database seeded: 6 users, 10 notes, 10 quiz results")
    print("Login with any username (pavan/pravinesh/ashwin/sneha/rahul/divya), password: test1234")

if __name__ == "__main__":
    seed()