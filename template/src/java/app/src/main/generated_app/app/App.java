/*
 * This source file was generated by the Gradle 'init' task
 */
package <%= projectNameSnake.downcase %>.app;


import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;


@SpringBootApplication
@RestController
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }

    @GetMapping("/hello")
    public String hello(
        @RequestParam(value = "name", defaultValue="World") String name
    ) {
        return String.format("Hello %s!", name);
    }
}