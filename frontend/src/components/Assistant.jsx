import React, { useState} from 'react'
import axios from 'axios'

const Assistant = () => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');

    const hundleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8004/api/v1/query/assistant', {question});
            setAnswer(response.data.answer);

        } catch (error) {

            setAnswer('Error fetching answer');

        }   
        
    }
return (
    <div>    <h1>Ask the Assistant</h1>
    <form onSubmit={hundleSubmit}>
        <input type="text"
        value={question}
        onChange={ (e) => setQuestion(e.target.value)}
        placeholder="Type your question here"
        required
         />
        <button type="submit">Ask</button>
    </form>
    {answer && (
        <div>
            <h2>Answer:</h2>
            <p>{answer}</p>
        </div>
    )}
    </div>

    )

}
export default Assistant;