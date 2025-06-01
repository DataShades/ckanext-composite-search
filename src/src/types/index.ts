interface SharedDefinition {
  placeholder?: string;
  default?: boolean;
  hidden?: boolean;
  label: string;
}

export interface TextDefinition extends SharedDefinition {
  type: "text";
}
export interface SelectDefinition extends SharedDefinition {
  type: "select";
  options: { label: string; value: any }[];
}

export type FieldDefinition = TextDefinition | SelectDefinition;

export type Definitions = { [key: string]: FieldDefinition };

export enum Junction {
  AND = "And",
  OR = "Or",
}

export interface FieldData {
  type: string;
  value?: any;
  junction?: Junction;
  negation?: boolean;
  id?: number;
}
