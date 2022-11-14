package ese589.decisiontree;

import java.util.List;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class DataReader {

    public static void read(String fileName) throws IOException {
        List<Entry> data = new ArrayList<>();
        BufferedReader reader = null;

        try {
            reader = new BufferedReader(new FileReader(fileName));
            String line = reader.readLine();
            while (line != null) {
                Entry entry = Entry.parseLine(line);
                if (entry != null) {
                    data.add(entry);
                }

                line = reader.readLine();
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        for (int i = 0; i < data.size(); i++) {
            System.out.println(data.get(i));
        }

        System.out.println(data.size());
    }

    public static void main(String[] args) {
        try {
            read("data/adult.data");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
