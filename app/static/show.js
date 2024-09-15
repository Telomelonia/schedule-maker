// Global variables to store data
let lessons, rooms, studentGroups, timeslots, teachers, subjectColors;

// Fetch JSON data from /get_solution endpoint
fetch('/get_solution')
    .then(response => response.json())
    .then(data => {
        console.log("Received data:", data);  // Debug log
        // Extract and store data
        lessons = data.lessons;
        rooms = data.rooms;
        studentGroups = data.student_groups;
        timeslots = data.timeslots.map(ts => {
            const match = ts.match(/start_time=(\d{2}:\d{2}:\d{2}), end_time=(\d{2}:\d{2}:\d{2})/);
            return { start_time: match[1], end_time: match[2] };
        });
        teachers = [...new Set(lessons.map(lesson => lesson.teacher))];
        subjectColors = data.subject_colors;

        console.log("Processed data:", { lessons, rooms, studentGroups, timeslots, teachers, subjectColors });  // Debug log

        // Initial render of the schedule
        renderSchedule('room');  // Default to grouping by room

        // Add event listeners to grouping buttons
        document.getElementById('group-by-student').addEventListener('click', () => renderSchedule('student'));
        document.getElementById('group-by-room').addEventListener('click', () => renderSchedule('room'));
        document.getElementById('group-by-teacher').addEventListener('click', () => renderSchedule('teacher'));
    })
    .catch(error => console.error('Error fetching data:', error));

function renderSchedule(groupBy) {
    console.log("Rendering schedule. Group by:", groupBy);  // Debug log
    const scheduleContainer = document.getElementById('schedule-container');
    if (!scheduleContainer) {
        console.error("Schedule container not found");  // Debug log
        return;
    }
    scheduleContainer.innerHTML = ''; // Clear previous content

    let entities;
    switch(groupBy) {
        case 'student':
            entities = studentGroups;
            break;
        case 'teacher':
            entities = teachers;
            break;
        case 'room':
        default:
            entities = rooms;
    }

    console.log("Entities to render:", entities);  // Debug log

    entities.forEach(entity => {
        const scheduleTable = createScheduleTable(entity, groupBy);
        scheduleContainer.appendChild(scheduleTable);
    });
}

function createScheduleTable(entity, groupBy) {
    console.log("Creating table for entity:", entity, "Group by:", groupBy);  // Debug log
    const table = document.createElement('table');
    table.className = 'schedule-table';

    // Create table header
    const headerRow = table.insertRow();
    const headerCell = headerRow.insertCell();
    headerCell.textContent = `Schedule for ${groupBy.charAt(0).toUpperCase() + groupBy.slice(1)}: ${entity}`;
    headerCell.colSpan = 2;

    // Create rows for each timeslot
    timeslots.forEach(timeslot => {
        const row = table.insertRow();
        const timeCell = row.insertCell();
        timeCell.textContent = `${timeslot.start_time} - ${timeslot.end_time}`;

        const lessonCell = row.insertCell();
        const lesson = findLesson(entity, timeslot, groupBy);
        if (lesson) {
            lessonCell.textContent = formatLessonText(lesson, groupBy);
            lessonCell.style.backgroundColor = subjectColors[lesson.subject];
        }
    });

    return table;
}

function findLesson(entity, timeslot, groupBy) {
    return lessons.find(lesson => {
        const matchesEntity = 
            groupBy === 'student' ? lesson.student_group === entity :
            groupBy === 'teacher' ? lesson.teacher === entity :
            lesson.room === entity;
        return matchesEntity && lesson.timeslot.includes(timeslot.start_time);
    });
}

function formatLessonText(lesson, groupBy) {
    switch(groupBy) {
        case 'student':
            return `${lesson.subject} (${lesson.teacher} - ${lesson.room})`;
        case 'teacher':
            return `${lesson.subject} (${lesson.student_group} - ${lesson.room})`;
        case 'room':
        default:
            return `${lesson.subject} (${lesson.student_group} - ${lesson.teacher})`;
    }
}

// Call renderSchedule when the page loads
document.addEventListener('DOMContentLoaded', () => renderSchedule('room'));