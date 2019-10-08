import csv
import random


def write_csv(dict_to_write, klassen, grootte):
    # Format csv location
    csv_location = "./data/%s_groepjes_per_%d.csv" % (
        "_".join(klassen),
        grootte
    )

    # newline="" zodat er geen rij wordt tussengelaten
    with open(csv_location, 'w', newline="") as csv_file:
        # Define writer object and fieldnames
        writer = csv.writer(csv_file)

        # Write horizontal headers
        writer.writerow([key for key in dict_to_write.keys()])

        # Write rows
        for i in range(len(dict_to_write["voornaam"])):
            to_write = [
                dict_to_write["voornaam"][i],
                dict_to_write["familienaam"][i],
                dict_to_write["geslacht"][i],
                dict_to_write["Geboortedatm"][i],
                dict_to_write["klasgroep"][i],
                dict_to_write["groep"][i],
            ]

            writer.writerow(to_write)


def read_csv():
    # Init
    csv_location = "./data/fast_groepen_opgave2.csv"
    columns = []

    # Get the data from the csv
    with open(csv_location) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if columns:
                for i, value in enumerate(row):
                    columns[i].append(value)
            else:
                # First row
                columns = [[value] for value in row]

    # Store data in dict
    return_dict = {col[0]: col[1:] for col in columns}

    return(return_dict)


def samenvatting():
    # Get unieke klasgroepen
    klasgroepen = sorted(list(set(data_dict["klasgroep"])))
    print("Er zijn %d klasgroepen" % len(klasgroepen))
    print("-"*75)

    # Init dict die de studenten per klasgroep bewaard
    klasgroep_dict = {}

    for klasgroep in klasgroepen:
        # Init klasgroep key als lege list
        klasgroep_dict[klasgroep] = []

        # Check voor alle studenten
        for index, individuele_klasgroep in enumerate(data_dict["klasgroep"]):
            # Check ofdat de student in de currently checked klasgroep zit
            if klasgroep == individuele_klasgroep:
                # indien dat het geval is,
                # voeg zijn/haar naam toe aan de list van deze klasgroep
                klasgroep_dict[klasgroep].append(
                    "%s %s" % (
                        data_dict["voornaam"][index],
                        data_dict["familienaam"][index]
                    )
                )

        print("In klasgroep %s zitten %d studenten" % (
            klasgroep,
            len(klasgroep_dict[klasgroep]))
        )
    print("-" * 75)

    # Init student_count
    studenten_mct = 0
    studenten_mit = 0

    # Check for every classgroup
    for klasgroep in klasgroepen:
        if 'MCT' in klasgroep:
            studenten_mct += len(klasgroep_dict[klasgroep])
        else:
            studenten_mit += len(klasgroep_dict[klasgroep])

    # User feedback
    print("Er zitten %d studenten in MCT" % studenten_mct)
    print("Er zitten %d studenten in MIT" % studenten_mit)
    print("-"*75)


def willekeurig_verdelen():
    size = input("Groepsgrootte: ")
    print("")

    try:
        # Check groepsgrootte input
        size = int(size)

        # stel user bepaalde vragen ivm de vorming/regels van de groepen
        mct = input("Zitten er studenten van MCT in de groepjes? (ja/nee) ")
        print("")

        mit = input("Zitten er studenten van MIT in de groepjes? (ja/nee) ")
        print("")

        print("Wilt u de groepjes vormen met studenten van "
              "1 of meerdere specifieke klasgroepen? ")
        print("Indien ja, gelieve de klasnamen alsvolgens te noteren: "
              "1MCT1, 1MCT2, 1MCT3, ... \nIndien neen, type \'neen\'")
        klassen = input("").strip()

        # Convert klassen input to list
        if ", " in klassen:
            klassen = klassen.split(", ")
            # Check of elke klas in de lijst van klassen staat
            if any(klassen) not in list(set(data_dict["klasgroep"])):
                # Indien een klas er niet in staat, is de input niet geldig
                print("Een of meerdere klassen werden niet herkend/ \
                        \nProbeer opnieuw\n")
                willekeurig_verdelen()
            else:
                # Indien geen enkele opgegeven klas niet geregistreerd is,
                # is de input geldig.
                klassen = sorted(list(set(klassen)))

        elif "nee" in klassen.lower():
            # Indien geen specifieke klassen werden opgegeven,
            # gaan alle klassen door naar de volgende stap
            klassen = sorted(list(set(data_dict["klasgroep"])))

        else:
            # Indien 1 klas werd opgegeven,
            # check of deze in de lijst van alle klassen staat
            if klassen.strip() in list(set(data_dict["klasgroep"])):
                klassen = [klassen.strip()]
            else:
                print("De input die u gaf als spefieke klasgroep werd niet herkend. \
                        \nProbeer opnieuw\n")
                willekeurig_verdelen()

        # Init list that will store students that
        # have passed the criteria given by user
        studenten_om_te_verdelen = []

        # Populate list with all students that pass the criteria given by user
        if type(klassen) == list:
            # Loop over all the students
            for index, voornaam in enumerate(data_dict["voornaam"]):
                # Fetch currently checked student's classgroup
                klasgroep = data_dict["klasgroep"][index]

                # Check whether the checked student passes given criteria
                if mct.lower() == "ja":
                    if "mct" in klasgroep.lower() and klasgroep in klassen:
                        # If he/she does, add him/her to the list of names
                        # to divide in groups later
                        studenten_om_te_verdelen.append(
                            "%s %s" % (
                                voornaam,
                                data_dict["familienaam"][index]
                            )
                        )

                if mit.lower() == "ja":
                    if "mit" in klasgroep.lower() and klasgroep in klassen:
                        # I could also insert the student randomly in the list
                        studenten_om_te_verdelen.append(
                            "%s %s" % (
                                voornaam,
                                data_dict["familienaam"][index]
                            )
                        )
        else:
            print("Er is iets fout gegaan met je input omtrent \
                    specifieke klassen. \nProbeer opnieuw\n")
            willekeurig_verdelen()

        # init dict that will store groepjes of random names
        random_groepjes = {}

        # Randomize list of students
        random.shuffle(studenten_om_te_verdelen)

        # Populate dict
        # Om de groepjes te vullen moeten we eerst het
        # totaal aantal studenten weten die verdeeld moeten worden
        for index, student in enumerate(studenten_om_te_verdelen):
            if int(index / size) not in random_groepjes.keys():
                random_groepjes[int(index / size)] = []
            random_groepjes[int(index / size)].append(student)

        # Init dict that will be stored in new csv
        new_dict = {}
        # Inherit keys van originele data
        for key in data_dict.keys():
            new_dict[key] = []
        # Voeg key toe voor de nieuwe groepen
        new_dict["groep"] = []

        for key in random_groepjes.keys():
            namen = [naam for naam in random_groepjes[key]]

            for i, naam in enumerate(namen):
                voornaam = str(naam.split(" ")[0])
                familienaam = " ".join(namen[i].split(" ")[1:])

                # Get indexes of the first name in the list of voornamen
                indexes_voornaam = [
                    i for i, e in enumerate(data_dict["voornaam"])
                    if e == voornaam
                ]
                # Get indexes of the surname in the list of surnames
                indexes_familienaam = [
                    i for i, e in enumerate(data_dict["familienaam"])
                    if e == familienaam
                ]
                # Make sure the indexes are the same
                current_indexes = list(
                    set(indexes_voornaam) & set(indexes_familienaam)
                )

                # Fetch remaining data
                geslacht = data_dict["geslacht"][current_indexes[0]]
                geboortedatum = data_dict["Geboortedatm"][current_indexes[0]]
                klasgroep = data_dict["klasgroep"][current_indexes[0]]
                # add selected students data to dict
                new_dict["voornaam"].append(voornaam)
                new_dict["familienaam"].append(familienaam)
                new_dict["geslacht"].append(geslacht)
                new_dict["Geboortedatm"].append(geboortedatum)
                new_dict["klasgroep"].append(klasgroep)
                new_dict["groep"].append(key)

            print(
                "Groepje %s: %s (=%d studenten)" % (
                    key,
                    ", ".join(namen),
                    len(random_groepjes[key])
                )
            )

        write_csv(new_dict, klassen, size)

    except ValueError:
        print("Gelieve een int op te geven als groepsgrootte\n")
        willekeurig_verdelen()

data_dict = read_csv()
samenvatting()
willekeurig_verdelen()
