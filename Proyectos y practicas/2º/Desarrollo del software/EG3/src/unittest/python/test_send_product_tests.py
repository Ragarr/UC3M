"""test for function 2"""
import unittest
from pathlib import Path

from freezegun import freeze_time
from uc3m_logistics.order_management_exception import OrderManagementException

from uc3m_logistics.order_manager import OrderManager


class MyTestCase(unittest.TestCase):
    """unittest class"""

    @freeze_time("2023-03-16")
    def test_valid(self):
        """test valid node"""
        my_order_manager = OrderManager()
        input_file = (
            str(Path.home().joinpath("PycharmProjects/G80.2023.T3.EG03/src/Json/test/valid.json"))
        )
        # pylint: disable=redefined-builtin
        hash = my_order_manager.send_product(input_file)
        self.assertEqual("e3966dc2cc732ab30f763a75bfb6b63ec1c48cc330cc3449d402e80507b3adeb", hash)

    @freeze_time("2023-03-16")
    def test_non_terminal_nodes(self):
        """Tests for non terminal nodes"""
        terminal_nodes = [5, 9, 25, 26, 27, 28, 17, 29, 30,
                          31, 32, 33, 34, 35, 36, 42, 43, 44, 45, 46, 47]
        non_terminal_nodes = [x for x in range(2, 48) if x not in terminal_nodes]

        my_order_manager = OrderManager()
        errors = 0

        for node in non_terminal_nodes:
            for add in ["delete", "duplicate"]:
                if node in [37, 39] and add == "duplicate":
                    continue
                input_file = (
                    str(
                        Path.home().joinpath(
                            "PycharmProjects/G80.2023.T3.EG03/src/Json/test/nodo"
                        )
                    )
                    + str(node)
                    + "_"
                    + add
                    + ".json"
                )

                try:
                    my_order_manager.send_product(input_file)
                    # el test debe fallar SIEMPRE con una excepcion controlada
                    # si no se eleva un error se cuenta como un fallo
                    print(f"the node {node} with {add} didnt raise an error")
                    errors += 1
                except OrderManagementException as error:
                    if error.message not in [
                        "Json Decode Error - Wrong Json format",
                        "Invalid order",

                    ]:
                        errors += 1
                        print(
                            f"Error not recognised in node: {node} "
                            f"with {add}. Error: {error.message}"
                        )

        if errors != 0:
            self.fail(f"{errors} Errors found")

    @freeze_time("2023-03-16")
    def test_terminal_nodes(self):
        """Tests for terminal nodes"""
        terminal_nodes = [5, 9, 25, 26, 27, 28, 17, 29, 30, 31,
                          32, 33, 34, 35, 36, 42, 43, 44, 45, 46, 47]
        my_order_manager = OrderManager()
        errors = 0
        for node in terminal_nodes:
            input_file = (
                    str(Path.home().joinpath("PycharmProjects/G80.2023.T3.EG03/src/Json/test/nodo"))
                    + str(node) + "_modification.json")

            try:
                my_order_manager.send_product(input_file)
                # el test debe fallar SIEMPRE con una excepcion controlada
                # si no se eleva un error se cuenta como un fallo
                print(f"the node {node} didnt raise an error")
                errors += 1
            except OrderManagementException as error:
                if error.message not in ["Json Decode Error - Wrong Json format", "Invalid order"]:
                    errors += 1
                    print(f"Error not recognised in node: {node}. Error: {error.message}")
        if errors != 0:
            self.fail(f"{errors} Errors found")


if __name__ == "__main__":
    unittest.main()
