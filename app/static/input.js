let timeslotCount = 0;
let roomCount = 0;
let lessonCount = 0;
$('#add_timeslot').click(function() {
    timeslotCount++;
    $('#timeslots').append(`
        <div>
            <label>Weekday: <input type="text" name="weekday_${timeslotCount - 1}" required></label>
            <label>Start Time: <input type="time" name="start_time_${timeslotCount - 1}" required></label>
            <label>End Time: <input type="time" name="end_time_${timeslotCount - 1}" required></label>
        </div>
    `);
    $('#timeslot_count').val(timeslotCount);
});

$('#add_room').click(function() {
    roomCount++;
    $('#rooms').append(`
        <div>
            <label>Room Name: <input type="text" name="room_name_${roomCount - 1}" required></label>
        </div>
    `);
    $('#room_count').val(roomCount);
});

$('#add_lesson').click(function() {
    lessonCount++;
    $('#lessons').append(`
        <div>
            <label>Subject: <input type="text" name="subject_${lessonCount - 1}" required></label>
            <label>Teacher: <input type="text" name="teacher_${lessonCount - 1}" required></label>
            <label>Group/Class: <input type="text" name="group_${lessonCount - 1}" required></label>
        </div>
    `);
    $('#lesson_count').val(lessonCount);

    
});
$('#sample_data').click(function() {
    $('#check_sample').val('true');
});