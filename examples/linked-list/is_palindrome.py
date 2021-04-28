from pydsa import validate_args
from pydsa.data_structures.linked_list import SinglyLinkedList

@validate_args
def is_palindrome(linked_list: SinglyLinkedList) -> bool:
    # Leetcode #234
    if linked_list.head is None:
        return True

    ll1 = linked_list.copy()
    middle_node = ll1.find_middle()
    
    # Split the linked list into two halves
    half2_ptr = middle_node.next_node
    middle_node.next_node = None
    
    # Reverse the second half
    ll2 = SinglyLinkedList()
    ll2.head = half2_ptr
    ll2.reverse()
    
    for node1, node2 in zip(ll1, ll2):
        if node1 != node2:
            return False
    return True


if __name__ == "__main__":
    def show_case(arr, expected):
        test_case = SinglyLinkedList(arr)
        result = is_palindrome(test_case)
        assert result == expected
        print(test_case, "is" if result else "is not", "a palindrome linked list.")

    show_case([1, 2, 2, 1], True)
    show_case([], True)
    show_case([1], True)
    show_case([1, 2, 3, 2, 1], True)
    show_case([1, 2, 3, 4, 2, 1], False)
    show_case([1, 2], False)
