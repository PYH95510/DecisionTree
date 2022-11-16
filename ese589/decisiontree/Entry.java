package ese589.decisiontree;

import ese589.decisiontree.Attributes.*;

public class Entry {
    public int age;
    public WorkClass workClass;
    public Education education;
    public int educationNum;
    public MaritalStatus maritalStatus;
    public Occupation occupation;
    public Relationship relationship;
    public Race race;
    public Sex sex;
    public int capital_gain;
    public int capital_loss;
    public int hoursPerWeek;
    public NativeCountry nativeCountry;
    public Income income;

    private Entry() {

    }

    public static Entry parseLine(String line) {
        Entry entry = new Entry();
        String[] splitLine = line.split(",");
        if (splitLine.length != 15) {
            System.out.println(String.format("Malformed line: {0}", line));
            return null;
        }

        try {
            entry.age = Integer.parseInt(splitLine[0].trim());
            entry.workClass = WorkClass.fromString(splitLine[1].trim());
            entry.education = Education.fromString(splitLine[3].trim());
            entry.educationNum = Integer.parseInt(splitLine[4].trim());
            entry.maritalStatus = MaritalStatus.fromString(splitLine[5].trim());
            entry.occupation = Occupation.fromString(splitLine[6].trim());
            entry.relationship = Relationship.fromString(splitLine[7].trim());
            entry.race = Race.fromString(splitLine[8].trim());
            entry.sex = Sex.fromString(splitLine[9].trim());
            entry.hoursPerWeek = Integer.parseInt(splitLine[12].trim());
            entry.nativeCountry = NativeCountry.fromString(splitLine[13].trim());
<<<<<<< HEAD

            entry.more50k = splitLine[14].trim().equals(">50K");
        } catch (NumberFormatException e) {
=======
            entry.income = Income.fromString(splitLine[14].trim());
        } catch (NumberFormatException e)
        {
>>>>>>> refs/remotes/origin/main
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
        sb.append(workClass).append(" ");
        sb.append(education).append(" ");
        sb.append(educationNum).append(" ");
        sb.append(maritalStatus).append(" ");
        sb.append(occupation).append(" ");
        sb.append(relationship).append(" ");
        sb.append(race).append(" ");
        sb.append(sex).append(" ");
        sb.append(hoursPerWeek).append(" ");
        sb.append(nativeCountry).append(" ");
        sb.append(income);
        return sb.toString();
    }
}
