import sys
sys.path.append('src')

from core.ontology_manager import OntologyManager

print("=" * 60)
print("TESTING ONTOLOGY MANAGER")
print("=" * 60)

# Test 1: Load ontology
print("\n1️⃣ Loading ontology...")
manager = OntologyManager("python_iteration_tutor.owl")

# Test 2: Get concepts
print("\n2️⃣ Getting concepts...")
concepts = manager.get_concepts()
print(f"   Found {len(concepts)} concepts:")
for i, c in enumerate(concepts, 1):
    print(f"   {i}. {c.name}")

# Test 3: Get concept details
print("\n3️⃣ Getting details for first concept...")
if concepts:
    details = manager.get_concept_details(concepts[0])
    print(f"   Name: {details['name']}")
    print(f"   Explanation: {details['explanation'][:60]}...")
    print(f"   Syntax: {details['syntax']}")
    if details['iterable']:
        print(f"   Iterable: {details['iterable']['name']}")
    if details['method']:
        print(f"   Method: {details['method']['name']}")

# Test 4: Get problems by level
print("\n4️⃣ Getting level 1 problems...")
problems_l1 = manager.get_problems_by_level(1)
print(f"   Level 1 problems: {len(problems_l1)}")

print("\n   Getting level 2 problems...")
problems_l2 = manager.get_problems_by_level(2)
print(f"   Level 2 problems: {len(problems_l2)}")

# Test 5: Get problem details
print("\n5️⃣ Getting problem details...")
if problems_l1:
    prob_details = manager.get_problem_details(problems_l1[0])
    print(f"   Problem: {prob_details['name']}")
    print(f"   Description: {prob_details['description'][:60]}...")
    print(f"   Difficulty: {'⭐' * prob_details['difficulty']}")
    print(f"   Concept needed: {prob_details['concept']}")
    print(f"   Test cases: {len(prob_details['test_cases'])}")

# Test 6: Get solution
print("\n6️⃣ Getting solution...")
if problems_l1:
    solution = manager.get_solution(problems_l1[0])
    if solution:
        print(f"   Solution code:")
        code_lines = solution['code'].split('\n')
        for line in code_lines[:3]:  # Show first 3 lines
            print(f"      {line}")
        print(f"      ...")

# Test 7: Get statistics
print("\n7️⃣ Getting statistics...")
stats = manager.get_statistics()
print(f"   📚 Concepts: {stats['concepts']}")
print(f"   ✏️  Problems: {stats['problems']}")
print(f"   ✅ Solutions: {stats['solutions']}")
print(f"   🧪 Test cases: {stats['test_cases']}")

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)