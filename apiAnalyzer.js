export async function analyzeAPI(apiUrl) {
    try {
        // Basic free API detection
        const isFree = !apiUrl.includes('premium') && 
                       !apiUrl.includes('paid') && 
                       !apiUrl.includes('enterprise');

        // Use AI to get more detailed description
        const aiDescription = await getAIAPIDescription(apiUrl);

        return {
            isFree: isFree,
            description: aiDescription || 'No description available'
        };
    } catch (error) {
        return {
            isFree: false,
            description: 'Unable to analyze API'
        };
    }
}

async function getAIAPIDescription(apiUrl) {
    try {
        const response = await fetch('/api/ai_completion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                prompt: `Analyze the purpose of this API based on its URL: ${apiUrl}. 
                Provide a brief, friendly description of what the API might do.
                
                interface APIDescription {
                    description: string;
                }
                
                {
                    "description": "This looks like a weather API that provides current temperature and forecast data for different locations."
                }`,
                data: apiUrl
            }),
        });

        const data = await response.json();
        return data.description || 'Unable to determine API purpose';
    } catch (error) {
        console.error('AI Analysis Error:', error);
        return 'Could not generate AI description';
    }
}