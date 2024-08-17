# HackerRank Contest Performance Tracker

This Python script retrieves performance data for all participants in a HackerRank contest. It collects leaderboard data and problem scores and outputs them to a CSV file.

## Features

- Fetches leaderboard data for all participants in a HackerRank contest.
- Retrieves problem-specific scores and consolidates them into a CSV file.

## Example

After running the script, you will get a CSV file named `leaderboard-<contest_slug>.csv`. Here's an example of what the CSV file might look like:

| name               | problem1-Sample-Easy | problem2-Biscuit Fest-Easy | ... | rank | score |
|--------------------|----------------------|----------------------------|-----|------|-------|
| user1              | 1                    | 0                          | ... | 1    | 1500  |
| user2              | 0                    | 1                          | ... | 2    | 1200  |


## Prerequisites

- Python 3.x installed on your machine


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/daken04/HackerRank-Contest-Performance-Tracker
   ```

2. Install the required Python packages:
   ```bash
   pip3 install requests
   ```

## Usage

1. Run the script
   ```bash
   python3 hackerrank_tracker.py
   ```

2. Follow the prompts to input your email and password.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Here's how you can help:

- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Make your changes and commit them (`git commit -m 'Add a new feature'`).
- Push to the branch (`git push origin feature-branch`).
- Open a pull request.

Please make sure your code adheres to our coding standards and includes tests where applicable.

## Contact

If you have any questions or need support, feel free to open an issue or contact me at [aryan.vermaav417@gmail.com].


