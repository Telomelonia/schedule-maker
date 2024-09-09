$(document).ready(function() {
    $('#startSolver').click(function() {
        $.get('/start_solver', function(data) {
            $('#status').text(data.message);
            checkStatus();
        });
    });

    function checkStatus() {
        $.get('/solver_status', function(data) {
            if (data.is_running) {
                $('#status').text('Solver is running...');
                setTimeout(checkStatus, 5000);  // Check again in 5 seconds
            } else if (data.has_solution) {
                $('#status').text('Solution ready!');
                getSolution();
            } else {
                $('#status').text('Solver stopped without finding a solution.');
            }
        });
    }

    function getSolution() {
        $.get('/get_solution', function(data) {
            if (data.error) {
                $('#solution').text(data.error);
            } else {
                // Here you would typically render the solution data
                // For simplicity, we're just showing the number of lessons
                $('#solution').text('Found ' + data.lessons.length + ' lessons.');
                // Show the redirect button
                $('#redirectButtonContainer').show();
            }
        });
    }

    $('#redirectButton').click(function() {
        window.location.href = '/show';
    });
});