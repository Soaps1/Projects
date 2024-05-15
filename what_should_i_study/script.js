document.getElementById('submit').addEventListener('click', function() {
    let interests = getCheckedValues('interests');
    let strengths = getCheckedValues('strengths');
    let careers = getCheckedValues('careers');

    let recommendations = getRecommendations(interests, strengths, careers);
    displayResults(recommendations);
});

function getCheckedValues(name) {
    let checkboxes = document.querySelectorAll(`input[name="${name}"]:checked`);
    let values = [];
    checkboxes.forEach((checkbox) => {
        values.push(checkbox.value);
    });
    return values;
}

function getRecommendations(interests, strengths, careers) {
    // Simple scoring system to recommend subjects
    let subjects = {
        'Mathematics': 0,
        'Science': 0,
        'Literature': 0,
        'History': 0,
        'Art': 0,
        'Music': 0,
        'Physical Education': 0
    };

    interests.forEach((interest) => {
        subjects[interest]++;
    });

    strengths.forEach((strength) => {
        subjects[strength]++;
    });

    careers.forEach((career) => {
        if (career === 'Engineering' || career === 'Medicine') {
            subjects['Mathematics']++;
            subjects['Science']++;
        } else if (career === 'Law' || career === 'Business') {
            subjects['Literature']++;
            subjects['History']++;
        } else if (career === 'Arts') {
            subjects['Art']++;
            subjects['Music']++;
        } else if (career === 'Sports') {
            subjects['Physical Education']++;
        }
    });

    let sortedSubjects = Object.keys(subjects).sort((a, b) => subjects[b] - subjects[a]);
    return sortedSubjects.slice(0, 3);
}

function displayResults(recommendations) {
    let resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<h2>Recommended Subjects:</h2><ul>${recommendations.map(subject => `<li>${subject}</li>`).join('')}</ul>`;
}
