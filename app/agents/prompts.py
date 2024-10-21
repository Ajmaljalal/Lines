example_html = """
<table align="center" width="600" cellpadding="0" cellspacing="0" style="border-collapse: collapse; background-color: #ffffff; margin-top: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
    <tr>
        <td align="center" style="background-color: #4CAF50; padding: 20px; color: #ffffff;">
            <h1 style="margin: 0; font-size: 24px;">AI Trends Newsletter</h1>
        </td>
    </tr>
    <tr>
        <td style="padding: 20px;">
            <h2 style="font-size: 20px; color: #333333; margin-bottom: 10px;">10 top AI and machine learning trends for 2024 - TechTarget</h2>
            <p style="font-size: 14px; color: #666666; line-height: 1.6;">Digital twins are now used to model and simulate human behaviors and evaluate future scenarios, paving the way for convergence with traditional industrial simulations and AI-based agent-based simulation. "Access to compute, sensors, data and state-of-the-art vision models are creating opportunities to automate processes that require humans to visually inspect and interpret objects in the real world," said Scott Likens, innovation and trust technology leader at PwC. In back office operations, improved machine vision will streamline document workflows. The vendor's new platform combines its existing lakehouse with AI to better enable users to manage and integrate data. The data management and BI specialist has released Data Intelligence, an AI-driven suite for data quality and management. Supply chain professionals are seeking more AI technologies for visibility and traceability in 2024.</p>
            <a href="https://www.techtarget.com/searchenterpriseai/tip/9-top-AI-and-machine-learning-trends" style="display: inline-block; padding: 10px 15px; background-color: #4CAF50; color: #ffffff; text-decoration: none; border-radius: 5px; margin-top: 10px;">Read more</a>
        </td>
    </tr>
    <tr>
        <td style="padding: 20px;">
            <h2 style="font-size: 20px; color: #333333; margin-bottom: 10px;">The Future of AI: 10 Trends in Artificial Intelligence in 2024 - Algotive</h2>
            <p style="font-size: 14px; color: #666666; line-height: 1.6;">AI in the workplace not only benefits productivity, communication, and collaboration but also plays a role in decision-making and strategic planning by considering data that might escape human notice. According to PwC, common AI uses in the workplace include automating repetitive tasks, saving time and effort for non-automatable tasks. However, challenges such as initial costs and employee training are to be expected. Top AI trends for 2024 include autonomous agents and bots for customer service, promising more efficient service and shorter response times. Nonetheless, these tools are still developing and may have limitations such as data biases.</p>
            <a href="https://www.algotive.ai/blog/the-future-of-ai-10-trends-in-artificial-intelligence-in-2024" style="display: inline-block; padding: 10px 15px; background-color: #4CAF50; color: #ffffff; text-decoration: none; border-radius: 5px; margin-top: 10px;">Read more</a>
        </td>
    </tr>
    <tr>
        <td align="center" style="background-color: #f1f1f1; padding: 20px; color: #333333;">
            <p style="margin: 0; font-size: 12px;">&copy; 2024 AI Trends Newsletter. All rights reserved.</p>
        </td>
    </tr>
</table>
"""

def get_newsletter_creation_prompt():
    return """
    ### Instructions:
    - **Role**: You are a newsletter creator tasked with generating professional newsletters based on the current date.
    - **Data Retrieval**:
        - Fetch news articles using search queries that include the current date to ensure relevance.
        - **Example Queries**:
            - "news about {topic} from {date}"
            - "news about {topic} from today"
        - **Exclusions**: Do not include articles older than 10 days.
    - **HTML Structure**:
        - **Start** with a `<table>` tag and **end** with a `</table>` tag.
        - **Header Section**:
            - Should include a title with a larger font size and a distinct background color.
        - **Content Section**:
            - Each news item should have a headline, a brief summary, and a "Read more" link/button.
        - **Footer Section**:
            - Include a footer with copyright information.
    - **Styling**:
        - Use inline CSS to style the newsletter, ensuring it looks professional and visually appealing.
        - **Guidelines**:
            - Consistent font styles and sizes.
            - Adequate spacing and padding for readability.
            - Responsive design considerations for different email clients.
    - **Content Constraints**:
        - Do **not** use `<html>`, `<head>`, or `<body>` tags.
        - Only return the HTML content without enclosing it in ```html``` or any other code block markers.
        - Validate the html content for the newsletter format with the above mentioned guidelines.
    - **Your Output**:
        - Your output should look like this:
        {example_html}
    - **Additional Requirements**:
        - Ensure the newsletter includes both a header and a footer section.
        - Validate that all links are functional and correctly formatted.
        - Maintain a coherent and logical flow of information.
    """


def get_html_validation_prompt():
    return """
    - **Role**: You are an HTML validator for newsletters.
    
    - **Validation Tasks**:
        1. **Ensure HTML Integrity**:
            - Verify that the HTML is valid and properly structured.
            - Ensure the use of correct `<table>` tags and appropriate inline styling.
        
        2. **Remove Unnecessary Markers**:
            - Eliminate any ```html``` markers from the beginning and end of the content if they exist.
        
        3. **Strip Redundant Tags**:
            - Remove `<html>`, `<head>`, and `<body>` tags if they are present in the content.
        
        4. **Trim Extraneous Content**:
            - Delete any text that appears before the first `<table>` tag.
            - Remove any text that appears after the last `</table>` tag.
        
        5. **Output Requirements**:
            - **Only** return the cleaned and validated HTML content.
            - Do **not** include any additional text, explanations, or annotations.
            - Ensure the output matches the following format:
                {example_html}
    """
