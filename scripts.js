// Function to fetch faculty data from the server
async function fetchFacultyData() {
    try {
        const response = await fetch('/get_faculty_data'); // Adjust the route as per your Flask setup
        const facultyData = await response.json();

        const facultyList = document.getElementById('facultyList');
        facultyData.forEach(faculty => {
            const facultyItem = document.createElement('li');
            facultyItem.innerHTML = `
                <h3>${faculty.first_name} ${faculty.last_name}</h3>
                <p>Department: ${faculty.department_name}</p>
                <p>Email: ${faculty.email}</p>
                <p>Phone: ${faculty.phone_number}</p>
                <p>Designation: ${faculty.designation}</p>
                <!-- Add more faculty details here -->
            `;
            facultyList.appendChild(facultyItem);
        });
    } catch (error) {
        console.error('Error fetching faculty data:', error);
    }
}

// Call the function to fetch and display faculty data
fetchFacultyData();
