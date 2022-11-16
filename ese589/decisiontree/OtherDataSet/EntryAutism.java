package ese589.decisiontree.OtherDataSet;

import ese589.decisiontree.OtherDataSet.AutismAttribute.*;

public class EntryAutism {

    public int age;
    public Sex sex;
    public Race race;
    public Jundice jundice;
    public Autism autism;
    public NativeCountry nativeCountry;
    public int resultNumeric;
    public Relationship relationship;

    private EntryAutism() {

    }

    public static EntryAutism parseLine(String line) {
        EntryAutism entry = new EntryAutism();
        String[] splitLine = line.split(",");
        if (splitLine.length != 21) {
            System.out.println(String.format("Malformed line: {0}", line));
            return null;
        }

        try {

            entry.relationship = Relationship.fromString(splitLine[7].trim());

            entry.age = Integer.parseInt(splitLine[10].trim());// done
            entry.sex = Sex.fromString(splitLine[11].trim()); // done
            entry.race = Race.fromString(splitLine[12].trim()); // done
            entry.jundice = Jundice.fromString(splitLine[13].trim());
            entry.autism = Autism.fromString(splitLine[14].trim());
            entry.nativeCountry = NativeCountry.fromString(splitLine[15].trim());
            entry.resultNumeric = Integer.parseInt(splitLine[17].trim());
            entry.relationship = Relationship.fromString(splitLine[19].trim());

        } catch (NumberFormatException e) {
            e.printStackTrace();
            return null;
        } catch (IllegalArgumentException e) {
            e.printStackTrace();
            return null;
        }
        return entry;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(age).append(" ");
        sb.append(sex).append(" ");
        sb.append(race).append(" ");
        sb.append(jundice).append(" ");
        sb.append(autism).append(" ");
        sb.append(nativeCountry).append(" ");
        sb.append(resultNumeric).append(" ");
        sb.append(relationship).append(" ");

        return sb.toString();
    }
}
