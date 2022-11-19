

def check_split(item_total, tax_rate, tip, people):
    """Calculate check value and evenly split.

       :param item_total: str (e.g. '$8.68')
       :param tax_rate: str (e.g. '4.75%)
       :param tip: str (e.g. '10%')
       :param people: int (e.g. 3)

       :return: tuple of (grand_total: str, splits: list)
                e.g. ('$10.00', [3.34, 3.33, 3.33])
    """
    
    # get the numbers from the strings
    item_total = float(item_total.strip('$'))
    tax_rate = float(tax_rate.strip('%')) / 100
    tip = float(tip.strip('%')) / 100
    print(item_total, tax_rate, tip, people)

    # calculate the grand total
    grand_total = (item_total * (1 + tax_rate)) * (1 + tip)
    print(grand_total)

    # calculate the split
    split = grand_total / people

    # round the split to 2 decimal places
    split = round(split, 2)

    # create a list of the splits
    splits = [split] * people

    # add the difference to the first split
    splits[0] += round(grand_total - split * people, 2)

    grand_total = round(grand_total, 2)

    assert grand_total == sum(splits)
    print(grand_total, splits)

    # convert the grand total to a string
    grand_total = f'${grand_total}'

    return grand_total, splits


if __name__ == '__main__':
    args = ('$141.86', '2%', '18%', 9)
    expected = '$170.75'

    grand_total, splits = check_split(*args)
    print(grand_total, expected)