const { exec } = require('child_process');

function runFetchScript() {
    console.log('Running fetch_sec_data.py...');
    exec('python3 fetch_sec_data.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing script: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout:\n${stdout}`);
    });
}

function scheduleFetch(intervalInHours) {
    console.log(`Scheduler started. Running every ${intervalInHours} hours.`);
    setInterval(runFetchScript, intervalInHours * 60 * 60 * 1000); 
}

scheduleFetch(6);
