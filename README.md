**Insider Trading Tracker**
The Insider Trading Tracker is a web application that fetches, processes, and displays insider trading data from SEC filings of the magnificent 7 companies. Users can view a summary of recent trades, view specific trade details, and visualize trading trends.

**How It's Made**
Tech used: Node.js, Express, PostgreSQL, Python, React, Chart.js

The backend is built with Node.js and Express, providing API endpoints to serve insider trading data. Data is fetched from SEC filings (in the SEC EDGAR website) using Python scripts and stored in a PostgreSQL database. The frontend is developed with React, offering an interactive user interface. Data visualizations are implemented using Chart.js to display trading trends effectively.

**Optimizations**
Future enhancements could include implementing pagination for large datasets, adding advanced filtering options like date ranges and transaction types, and incorporating user authentication to secure access to sensitive data. 

**Lessons Learned**
Handling real-time data updates and ensuring efficient data processing were the most challenging butrewarding aspects. Additionally, creating interactive data visualizations highlighted the creativity needed for presenting complex data in a user-friendly manner.
