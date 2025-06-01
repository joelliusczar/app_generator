package <%= projectNameSnake.downcase %>.engine.utilities;

import <%= projectNameSnake.downcase %>.engine.interfaces.FriendlyNameable;
import <%= projectNameSnake.downcase %>.engine.dtos.NamedId;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class EnumUtils {
	public static <E extends Enum<E> & FriendlyNameable> List<NamedId>
	getNamedIds(Class<E> e)
	{
		return Arrays.stream(e.getEnumConstants())
			.map((var c) -> new NamedId(c.ordinal(), c.getFriendlyName()))
			.collect(Collectors.toList());
	}
}