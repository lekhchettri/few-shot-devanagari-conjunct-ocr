# Few-Shot Devanagari OCR: Prototypical Networks for Low-Resource Character Recognition

This repository contains the complete code and notebook for a self-directed few-shot meta-learning project focused on recognizing highly complex, handwritten **Devanagari Conjunct Consonants**.

The project addresses the fundamental challenge of **data scarcity** in Indic script OCR by training a model to generalize from only a handful of examples per class.

---

## 🚀 Methodology and Results

The system utilizes a **Prototypical Network** architecture, a metric-based approach, to learn a robust feature embedding space where classification is performed purely by calculating the Euclidean distance to calculated class centroids (prototypes).

### Key Features:

* **Meta-Learning Paradigm:** Implements full episodic training to simulate and solve the $N$-Way $K$-Shot classification problem.
* **Architecture:** Uses a **MobileNetV2** backbone (frozen for feature extraction) with a **trainable Dense head** to learn the optimal 64-dimensional embedding metric.
* **Data Strategy:** Incorporates geometric data augmentation (rotations) and handles highly sparse class distributions using a custom retry mechanism for stable training.

### Performance (5-Way Classification on Unseen Characters):

| Setting | Accuracy | Interpretation |
| :--- | :--- | :--- |
| **5-Shot (K=5)** | $\approx \mathbf{77.58\%}$ | High generalization using only 5 support samples per character. |
| **1-Shot (K=1)** | $\approx \mathbf{63.57\%}$ | Strong performance from a single example, demonstrating robust metric learning. |

---

## 🗃️ Dataset and Setup

### Dataset Link (DevaConj-FSL)

The full handwritten dataset of 210 Devanagari Conjunct character classes is hosted separately on Kaggle due to its size:

**[Devanagari Conjunct Characters - Handwritten Images](https://www.kaggle.com/datasets/lekhnath/devanagari-conjunct-characters-handwritten-images)**

### Repository Contents

* `devanagari-conjunct-ocr-few-shot.ipynb`: The final Jupyter Notebook containing all data loading, augmentation, the Prototypical Network class definitions, and the training/evaluation loops.
* `requirements.txt`: Python package dependencies needed to run the notebook.

### Local Setup

1.  **Clone the Repository:**
    ```bash
    git clone git@github.com:lekhchettri/few-shot-devanagari-conjunct-ocr.git
    cd few-shot-devanagari-conjunct-ocr
    ```
2.  **Download Data:** Download the dataset from the Kaggle link above. Ensure the **`main/`** folder containing all 210 subfolders is placed into the root directory of this repository.
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run:** Open and execute the notebook.
