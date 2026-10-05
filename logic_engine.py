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

    def forward_chain(self):
        """
        Data-Driven Forward Chaining algorithm.
        Iterates through rules and infers new facts until no more facts can be deduced.
        """
        new_facts_added = True

        while new_facts_added:
            new_facts_added = False

            for premises, conclusion in self.rules:
                if conclusion not in self.facts:
                    # Modus Ponens Check: check if all premises are present in facts
                    if all(p in self.facts for p in premises):
                        self.facts.add(conclusion)
                        new_facts_added = True
