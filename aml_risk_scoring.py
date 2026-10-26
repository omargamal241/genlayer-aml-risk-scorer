from genlayer import *

class AMLRiskScorer:
    """
    Intelligent Contract on GenLayer for autonomous on-chain AML risk assessment
    using LLM-powered consensus logic.
    """
    admin: Address
    high_risk_threshold: int
    evaluated_records: TreeMap[str, str]

    def __init__(self, high_risk_threshold: int = 70):
        self.admin = msg.sender
        self.high_risk_threshold = high_risk_threshold
        self.evaluated_records = TreeMap[str, str]()

    @view
    def get_risk_assessment(self, tx_id: str) -> str:
        """Fetch previously stored assessment result for a given transaction."""
        return self.evaluated_records.get(tx_id, "Transaction record not found")

    @write
    def evaluate_transaction(
        self,
        tx_id: str,
        sender_address: str,
        recipient_address: str,
        amount_usd: int,
        tx_frequency_per_hour: int,
        is_known_mixer_related: bool,
    ) -> str:
        """
        Executes an AI-based AML risk evaluation using GenLayer's non-deterministic consensus.
        Validators run the LLM prompt to score the risk and agree on the verdict.
        """
        prompt = f"""
        You are an institutional AML (Anti-Money Laundering) compliance validator.
        Evaluate the transaction risk score from 0 to 100 based on these details:
        - Transaction ID: {tx_id}
        - Sender: {sender_address}
        - Recipient: {recipient_address}
        - Volume USD: ${amount_usd}
        - Hourly Frequency: {tx_frequency_per_hour} txs/hour
        - Interacted with Mixer/Tornado: {is_known_mixer_related}

        Risk rules:
        - Interaction with mixers automatically adds +40 risk.
        - High frequency (>20 txs/hour) with large amounts adds +30 risk.
        - Amounts over $100,000 add +20 risk.

        Respond strictly in this format:
        SCORE: <number between 0 and 100> | STATUS: <LOW_RISK/MEDIUM_RISK/HIGH_RISK> | REASON: <concise reason>
        """

        # Invoking LLM via GenLayer consensus
        eval_result = gl.exec_prompt(prompt)

        # Store the consensus outcome permanently on-chain
        self.evaluated_records[tx_id] = eval_result
        return eval_result

    @write
    def update_threshold(self, new_threshold: int):
        """Allows contract owner to adjust high risk score boundary."""
        assert msg.sender == self.admin, "Unauthorized: Only admin can update threshold"
        assert 0 <= new_threshold <= 100, "Threshold must be between 0 and 100"
        self.high_risk_threshold = new_threshold
