/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package fun.mingshan.markdown4j.encoder.element;

import fun.mingshan.markdown4j.type.element.BoldElement;
import fun.mingshan.markdown4j.type.element.Element;
import fun.mingshan.markdown4j.type.element.ElementType;

/**
 * @author hanjuntao
 * @date 2022/1/18
 */
@SuppressWarnings("ALL")
public class BoldElementEncoder implements ElementEncoder {
    @Override
    public String encode(Element element) {
        BoldElement boldElement = (BoldElement) element;

        return "**" + boldElement.getContent() + "**";
    }

    @Override
    public ElementType getType() {
        return ElementType.BOLD;
    }
}
