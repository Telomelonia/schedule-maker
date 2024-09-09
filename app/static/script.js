// Fetch JSON data from /get_solution endpoint
fetch('/get_solution')
    .then(response => response.json())
    .then(data => {
        // Extract lessons, rooms, student groups, and timeslots
        const lessons = data.lessons;
        const rooms = data.rooms;
        const studentGroups = data.student_groups;
        const timeslots = data.timeslots.map(ts => {
            const match = ts.match(/start_time=(\d{2}:\d{2}:\d{2}), end_time=(\d{2}:\d{2}:\d{2})/);
            return { start_time: match[1], end_time: match[2] };
        });

        // Create schedule table
        const scheduleTable = document.createElement('table');
        scheduleTable.id = 'schedule-table';

        // Create table headers
        const tableHeaders = ['Time', ...rooms];
        const tableHeaderRow = document.createElement('tr');
        tableHeaders.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            tableHeaderRow.appendChild(th);
        });
        scheduleTable.appendChild(tableHeaderRow);

        // Create table rows for each timeslot
        timeslots.forEach(timeslot => {
            const tableRow = document.createElement('tr');
            const timeCell = document.createElement('td');
            timeCell.textContent = `${timeslot.start_time} - ${timeslot.end_time}`;
            tableRow.appendChild(timeCell);

            // Create cells for each room
            rooms.forEach(room => {
                const cell = document.createElement('td');
                const lessonsInRoom = lessons.filter(lesson => 
                    lesson.room === room && lesson.timeslot.includes(timeslot.start_time)
                );
                if (lessonsInRoom.length > 0) {
                    const lesson = lessonsInRoom[0];
                    cell.style.backgroundColor = data.subject_colors[lesson.subject];
                    cell.textContent = `${lesson.subject} (${lesson.student_group})`;
                }
                tableRow.appendChild(cell);
            });

            scheduleTable.appendChild(tableRow);
        });

        // Append schedule table to container
        document.getElementById('schedule-container').appendChild(scheduleTable);
    })
    .catch(error => console.error('Error fetching data:', error));