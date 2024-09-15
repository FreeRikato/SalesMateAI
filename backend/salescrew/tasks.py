from textwrap import dedent
from crewai import Task


class SalesMateTasks:
    def research_task(
        self, agent, prospect_name, company_name, prospect_additional_information
    ):
        return Task(
            description=dedent(
                f"""\
                    As a sales development research agent focused on prospect research, your primary responsibility is to identify and analyze potential leads for the sales team by thoroughly researching target company, key decision-makers, and industry trends. You will leverage various tools, databases, and social media platforms to gather valuable insights on prospects, including company size, revenue, pain points, and market positioning. Your role involves creating detailed prospect profiles, prioritizing leads based on their fit with the company's ideal customer profile, and continuously monitoring industry news and competitor activity to keep the sales team informed of new opportunities. Your research will be pivotal in driving sales outreach strategies and increasing the overall efficiency of the sales pipeline.
                    
                    Prospect Name: {prospect_name}
                    Company Name: {company_name}
                    Additional Information: {prospect_additional_information}
                """
            ),
            expected_output=dedent(
                f"""\
                    The expected output should be a detailed prospect profile that includes the company's background, key decision-makers with contact information, relevant business metrics (such as revenue and employee count), industry insights, and any recent news or developments. Additionally, the profile should highlight the prospect’s potential pain points or areas where they could benefit from the company's offerings, along with a priority ranking based on how well the prospect aligns with the ideal customer profile. This output will help the sales team tailor their outreach and increase the likelihood of engagement.
                                     """
            ),
            agent=agent,
        )

    def write_email_task(self, agent, product_catalog):
        return Task(
            description=dedent(
                f"""\
                    As a sales development email writing agent, your primary responsibility is to craft compelling, personalized outreach emails based on the prospect research and a deep understanding of the company's product catalog. You will use the insights gathered from the prospect’s background, including their pain points, industry trends, and key decision-makers, to tailor each email with a personalized approach that highlights how the company's products or services can solve specific challenges or add value to their business. Your emails should be concise, engaging, and action-oriented, with a focus on building rapport and encouraging the recipient to take the next step in the sales process, whether that's scheduling a call or requesting more information. Each email must align with the company’s tone and sales strategy, ensuring a high level of professionalism and impact.
                    
                    Product Catalog: {product_catalog}
                """
            ),
            expected_output=dedent(
                f"""\
                    The expected output should be a well-structured, personalized email that starts with an attention-grabbing subject line and a personalized greeting. The body should include a clear connection between the prospect’s business needs, as identified through research, and the specific products or services that can address those needs. The email should be concise, with a focus on the value proposition, and include a clear call-to-action (e.g., scheduling a call or meeting). The tone should be professional yet approachable, and it should be tailored to the recipient’s role and company, avoiding generic or templated language.
                    """,
            ),
            agent=agent,
        )

    def review_email_task(self, agent, template):
        return Task(
            description=dedent(
                f"""\
                You are an email review agent for a sales development research team, responsible for ensuring that each generated email aligns with the company's sales email templates and winning email examples. Your primary task is to carefully review the personalized sales emails, ensuring they adhere to best practices such as clear subject lines, personalized greetings, engaging opening lines, relevance to the prospect's business or pain points, clear call-to-action, and a professional tone. You must ensure the email is concise, free of grammatical errors, and tailored to the recipient while maintaining a focus on driving conversions and fostering engagement. Evaluate each email's structure, language, and tone for alignment with the company's standards of success.
                
                Sales Email Template / Winning Emails: {template}
                """
            ),
            expected_output=dedent(
                f"""\
                The expected output is a concise, well-structured email that follows the company's sales email template, personalized for the recipient, and adheres to best practices. It should have a clear subject line, a strong opening, relevant and engaging content, and a compelling call-to-action. The tone must be professional yet approachable, free from errors, and focused on addressing the prospect’s needs while driving engagement.
                """
            ),
            agent=agent,
        )
