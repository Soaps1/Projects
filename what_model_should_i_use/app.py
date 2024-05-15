from flask import Flask, render_template, request

app = Flask(__name__)

def select_model(nature, target, goal, dataset_size, interpretability):
    if nature == "supervised":
        if target == "categorical":
            if interpretability == "yes":
                return ["Logistic Regression", "Decision Trees"]
            else:
                return ["Random Forest", "Gradient Boosting", "Neural Networks"]
        elif target == "continuous":
            if interpretability == "yes":
                return ["Linear Regression", "Lasso", "Ridge Regression"]
            else:
                return ["Decision Trees", "Random Forest", "Gradient Boosting", "Neural Networks"]
    elif nature == "unsupervised":
        if goal == "clustering":
            return ["K-means", "DBSCAN", "Agglomerative Clustering"]
        elif goal == "dimensionality_reduction":
            return ["PCA", "SVD", "t-SNE", "UMAP"]
    elif nature == "semi-supervised":
        return ["Self-training", "Co-training", "Semi-supervised SVMs", "Generative Models"]
    elif nature == "reinforcement":
        return ["Q-learning", "Deep Q-Networks", "Policy Gradient Methods", "Actor-Critic Methods"]
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    models = []
    if request.method == 'POST':
        nature = request.form['nature']
        target = request.form.get('target')
        goal = request.form.get('goal')
        dataset_size = request.form['dataset_size']
        interpretability = request.form['interpretability']
        models = select_model(nature, target, goal, dataset_size, interpretability)
    return render_template('index.html', models=models)

if __name__ == '__main__':
    app.run(debug=True)
