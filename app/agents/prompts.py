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
    # Newsletter Creation Instructions
    
    ## Core Requirements
    - Create an HTML email newsletter about the topic provided by the user
    - Use only inline CSS styling
    - Content must be structured within a single `<table>` element
    - Maximum width: 600px

    ## Structure Requirements

    1. Header Section styled with inline CSS (Required)
        <tr>
            <td>
                <h1>{topic}</h1>
            </td>
        </tr>


    2. Content Sections styled with inline CSS (2-4 articles)
    - Each article must have:
    <tr>
        <td>
            <h2>{Article Title}</h2>
            <p>{Summary}</p>
            <a href="{URL}">Read more</a>
        </td>
    </tr>
    

    3. Footer Section styled with inline CSS (Required)
    <tr>
        <td>
            <p>{&copy; ...}</p>
        </td>
    </tr>
    

    ## Content Guidelines

    DO:
    - Use current news (within last 7 days)
    - Include source attribution for each article
    - Use `<style>` tags and inline styling
    - Keep summaries between 100-150 words
    - Use proper HTML entity encoding for special characters
    - Ensure all links are properly formatted with https://

    DON'T:
    - Include external CSS or JavaScript
    - Add `<html>`, `<head>`, or `<body>` tags
    - Include relative URLs

    ## Validation Steps
    1. Verify table structure:
    - Must start with `<table align="center" width="600"`
    - Must end with `</table>`
    - Must have all three sections (header, content, footer)

    2. Check content formatting:
    - All styles must be inline
    - All colors must use hex codes
    - All measurements must use px units
    - All links must be absolute URLs

    3. Verify responsiveness:
    - Use percentage-based widths for inner content
    - Include proper cellpadding and cellspacing
    - Set border-collapse: collapse

    ## Error States
    If unable to fetch current news:
    - Keep structure intact
    - Mark newsletter as "Preview Version"

    ## Your output should look like this:
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

    ## Yout output should **NOT** look like this, because it is not embedded in a <table> and its child tags: 
    "Based on today's breaking news, Anthropic has made a significant announcement about their AI technology. Here are the key points from the news:
    1. Anthropic has released an updated version of Claude 3.5 Sonnet with a new "Computer Use" feature that allows it to interact with PC applications.
    2. The AI can analyze screen contents and take actions on behalf of users.
    3. The technology is being released in beta to developers after limited testing.
    4. This development puts Anthropic in direct competition with OpenAI in the race to develop AI agents capable of complex task automation.

    The news has been covered by multiple major outlets including TechCrunch, Bloomberg, and CNBC, indicating the significance of this announcement."


    """
