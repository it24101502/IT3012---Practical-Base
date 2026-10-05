class KnowledgeBase:
    """
    A declarative Knowledge Base (KB) that stores facts and Horn Clause rules.
    """

    def __init__(self):
        # Declare facts as a Set to store unique string facts
        self.facts = set()
        # Declare rules as a List to store tuples: ([list_of_premises], "conclusion_string")
        self.rules = []

    def tell_fact(self, fact_string: str):
        """Adds a unique fact string to the facts set."""
        self.facts.add(fact_string)

    def tell_rule(self, premise_list: list, conclusion_string: str):
        """Appends a rule tuple ([premises], conclusion) to the rules list."""
        self.rules.append((premise_list, conclusion_string))

    def clear_facts(self):
        """Empties the facts set."""
        self.facts.clear()

'''
if __name__ == "__main__":
    kb = KnowledgeBase()

    # Add facts
    kb.tell_fact("TargetVisible")
    kb.tell_fact("HasAmmo")

    # Add a Horn clause rule: IF TargetVisible AND HasAmmo THEN CanShoot
    kb.tell_rule(["TargetVisible", "HasAmmo"], "CanShoot")

    print("Facts:", kb.facts)
    print("Rules:", kb.rules)

    # Clear facts
    kb.clear_facts()
    print("Facts after clearing:", kb.facts)
'''