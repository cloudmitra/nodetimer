const { app } = require('@azure/functions');
const appInsights = require("applicationinsights");
const axios = require("axios");
const fs = require("fs");
appInsights.setup("00000000-0000-0000-0000-000000000000").start();
const client = appInsights.defaultClient;
app.timer('timerTrigger1', {
    schedule: '0 */1 * * * *',
    handler: (myTimer, context) => {
        const currentEnv = process.env.env || "dev"; // Default to 'dev' if not set
        const data = fs.readFileSync("endpoint.json");
        const config = JSON.parse(data);
        const environment = config.environments.find(env => env.name === currentEnv);
        if (!environment) {
            context.log.error(`Environment '${currentEnv}' not found in configuration.`);
            return;
        }
        for (const endpoint of environment.endpoints) {
            const name = `${environment.name} - ${endpoint.name}`;
            console.log(name);
            const url = endpoint.url;
            console.log(url);
            const apiStartTime = new Date();
            const apiEndTime = new Date();
            try {
                
                const response =  axios.get(url);
                const duration = apiEndTime - apiStartTime;
    
                // Log availability as success
                client.trackAvailability({
                    name: name,
                    success: true,
                    duration: duration,
                    message: `API responded with status ${response.status}`,
                    time: apiStartTime,
                    runLocation: "Azure Function",
                    id: context.invocationId
                });
                context.log(`Available: ${name} (${response.status})`);
            } catch (error) {
                const apiEndTime = new Date();
                const duration = apiEndTime - apiStartTime;
    
                // Log availability as failure
                client.trackAvailability({
                    name: name,
                    success: false,
                    duration: duration,
                    message: `Error pinging API: ${error.message}`,
                    time: apiStartTime,
                    runLocation: "Azure Function",
                    id: context.invocationId
                });
                context.log.error(`Unavailable: ${name} (${error.message})`);
            }
        }
    }
});