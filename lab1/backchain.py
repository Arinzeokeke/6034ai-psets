from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    # make a lists of antes from rules with subs that 
    # match our hyp
    matched_rules = []
    for rule in rules:
        consequent = list(rule.consequent())
        #print consequent, hypothesis
        mapping = [ match(each, hypothesis) for each in consequent if match(each, hypothesis) or hypothesis == each ]
        if mapping:
            mapping = mapping[0]
            print mapping
            antecedent = rule.antecedent()
            print antecedent
            if isinstance(antecedent, str):
                matched_rule = AND([populate(antecedent, mapping)])
            else:
                matched_rule = type(antecedent)([ populate(x, mapping) for x in list(antecedent) ])
            matched_rules.append(matched_rule)

    # if nothing found, return the hyp
    if not matched_rules:
        return hypothesis
    return simplify(OR([ hypothesis ] + [ type(hyp)([backchain_to_goal_tree(rules, each) for each in hyp]) for hyp in matched_rules ]))

    # else (if something found. we have a list of antecs)
    # return an OR of current hypothesis joined with
    #for each of matched rules ( all in the or)
    #a list comprehension where each of the elems wrapped in
    # a recursive call
        # return OR( [ backchain_to_goal_tree(rules, hyp) for hyp in matched_rules])

# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
